import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../models/dummy_data.dart';
import '../widgets/score_card.dart';
import '../widgets/quick_action_button.dart';
import '../widgets/activity_feed_item.dart';
import '../widgets/practitioner_card.dart';
import '../widgets/wearable_widget.dart';
import '../widgets/premium_icons.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final healthScore = DummyData.currentHealthScore;

    return Scaffold(
      backgroundColor: AppTheme.lightCream,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Welcome back, Alex',
                        style: Theme.of(context).textTheme.headlineMedium,
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Tuesday, November 12, 2024',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                  IconButton(
                    icon: const Icon(Icons.notifications_outlined),
                    onPressed: () {},
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Today's Wellness Summary Card
              GlassmorphicCard(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        PremiumIcon(
                          icon: Icons.favorite_rounded,
                          gradientColors: PremiumIcon.healingGradient,
                          size: 28,
                          iconSize: 14,
                          borderRadius: 8,
                        ),
                        const SizedBox(width: 10),
                        Text(
                          'Today\'s Wellness',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.w600,
                              ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),

                    // SANA Health Score
                    Row(
                      children: [
                        Expanded(
                          child: ScoreCard(
                            title: 'SANA Score',
                            score: healthScore.overall,
                            change: 3.0,
                            subtitle: healthScore.status,
                            color: AppTheme.getStatusColor(healthScore.status),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            children: [
                              _buildQuickMetric(
                                context,
                                'Mood',
                                Icons.sentiment_very_satisfied_rounded,
                                PremiumIcon.healingGradient,
                                'Good',
                              ),
                              const SizedBox(height: 6),
                              _buildQuickMetric(
                                context,
                                'Energy',
                                Icons.bolt_rounded,
                                PremiumIcon.vitalityGradient,
                                '7/10',
                              ),
                              const SizedBox(height: 6),
                              _buildQuickMetric(
                                context,
                                'Sleep',
                                Icons.bedtime_rounded,
                                PremiumIcon.calmGradient,
                                '7.5h',
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Quick Actions
              Text(
                'Quick Actions',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  QuickActionButton(
                    icon: Icons.edit_note,
                    label: 'Log Symptoms',
                    onTap: () {},
                  ),
                  QuickActionButton(
                    icon: Icons.calendar_today,
                    label: 'Book Appointment',
                    onTap: () {},
                  ),
                  QuickActionButton(
                    icon: Icons.book,
                    label: 'Write Journal',
                    onTap: () {},
                  ),
                  QuickActionButton(
                    icon: Icons.chat,
                    label: 'Message',
                    onTap: () {},
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Upcoming Appointments
              if (DummyData.upcomingAppointments.isNotEmpty) ...[
                Text(
                  'Upcoming Appointments',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 12),
                _buildAppointmentCard(context, DummyData.upcomingAppointments[0]),
                const SizedBox(height: 24),
              ],

              // Recent Activity
              Text(
                'Recent Activity',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 12),
              ...DummyData.recentActivity.take(4).map((activity) {
                return ActivityFeedItem(activity: activity);
              }),
              const SizedBox(height: 24),

              // Wearable Data
              Text(
                'Wearable Data',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: DummyData.wearableData.map((data) {
                  return WearableWidget(data: data);
                }).toList(),
              ),
              const SizedBox(height: 24),

              // Recommended Practitioners
              Text(
                'Recommended for You',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 8),
              Text(
                'Based on your anxiety tracking, these practitioners specialize in stress management',
                style: Theme.of(context).textTheme.bodySmall,
              ),
              const SizedBox(height: 12),
              SizedBox(
                height: 200,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: DummyData.recommendedPractitioners.length,
                  itemBuilder: (context, index) {
                    return Container(
                      width: 280,
                      margin: const EdgeInsets.only(right: 12),
                      child: PractitionerCard(
                        practitioner: DummyData.recommendedPractitioners[index],
                      ),
                    );
                  },
                ),
              ),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildQuickMetric(
    BuildContext context,
    String label,
    IconData icon,
    List<Color> gradientColors,
    String value,
  ) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          PremiumIcon(
            icon: icon,
            gradientColors: gradientColors,
            size: 32,
            iconSize: 16,
            borderRadius: 10,
            hasShadow: false,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: AppTheme.textLight,
                        fontSize: 11,
                      ),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        fontWeight: FontWeight.w600,
                        fontSize: 13,
                      ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAppointmentCard(BuildContext context, Appointment appointment) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
                const CircleAvatar(
                  radius: 20,
                  child: Icon(Icons.person, size: 20),
                ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    appointment.practitioner.name,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    appointment.practitioner.specialty,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(Icons.calendar_today, size: 14, color: AppTheme.textSecondary),
                      const SizedBox(width: 4),
                      Text(
                        'Nov 15, 2:30 PM',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                ],
              ),
            ),
            Icon(
              Icons.chevron_right,
              color: AppTheme.textLight,
            ),
          ],
        ),
      ),
    );
  }
}
