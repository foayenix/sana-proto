import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../theme/app_theme.dart';
import '../models/dummy_data.dart';
import '../widgets/premium_icons.dart';

class PractitionerProfileScreen extends StatelessWidget {
  final Practitioner practitioner;

  const PractitionerProfileScreen({super.key, required this.practitioner});

  @override
  Widget build(BuildContext context) {
    final breakdown = DummyData.sanaIndexBreakdown;

    return Scaffold(
      backgroundColor: AppTheme.lightCream,
      body: CustomScrollView(
        slivers: [
          // App Bar with Practitioner Image
          SliverAppBar(
            expandedHeight: 200,
            pinned: true,
            backgroundColor: AppTheme.primaryGreen,
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [
                      AppTheme.primaryGreen.withOpacity(0.8),
                      AppTheme.primaryGreen,
                    ],
                  ),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const SizedBox(height: 40),
                    const CircleAvatar(
                      radius: 52,
                      child: Icon(Icons.person, size: 52),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      practitioner.name,
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    Text(
                      practitioner.title,
                      style: const TextStyle(
                        fontSize: 14,
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          // Content
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // SANA Index Score Card
                  Container(
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [Color(0xFF4A7C59), Color(0xFF3D6B4A)],
                      ),
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: AppTheme.primaryGreen.withOpacity(0.3),
                          blurRadius: 16,
                          offset: const Offset(0, 6),
                        ),
                      ],
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.2),
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: const Icon(Icons.verified_rounded, color: Colors.white, size: 22),
                              ),
                              const SizedBox(width: 10),
                              const Text(
                                'SANA Index',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w600,
                                  color: Colors.white,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          PremiumSanaIndex(
                            score: practitioner.sanaIndex,
                            size: 90,
                            showLabel: false,
                          ),
                          const SizedBox(height: 12),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(16),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.emoji_events_rounded, color: Color(0xFFFFD700), size: 18),
                                const SizedBox(width: 6),
                                const Text(
                                  'Top 10% of Herbalists',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.w500,
                                    fontSize: 13,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Score Breakdown
                  Text(
                    'Score Breakdown',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  _buildBreakdownItem(
                    context,
                    'Verified Credentials',
                    Icons.verified_user_rounded,
                    PremiumIcon.successGradient,
                    breakdown.credentials,
                    20,
                    [
                      'Degree: BSc Herbal Medicine (University of Westminster)',
                      '${practitioner.yearsExperience} years experience',
                      'CNHC registered',
                      'Professional indemnity insurance',
                    ],
                  ),
                  _buildBreakdownItem(
                    context,
                    'Treatment Volume',
                    Icons.bar_chart_rounded,
                    PremiumIcon.trustGradient,
                    breakdown.treatmentVolume,
                    20,
                    [
                      '${practitioner.clientsGraduated}+ clients treated',
                      '${practitioner.totalSessions}+ sessions logged',
                      '${practitioner.yearsExperience} years on platform',
                    ],
                  ),
                  _buildBreakdownItem(
                    context,
                    'Measured Outcomes',
                    Icons.trending_up_rounded,
                    PremiumIcon.healingGradient,
                    breakdown.measuredOutcomes,
                    40,
                    [
                      'Average improvement: 67%',
                      'Effect size: 0.82 (large)',
                      'Client retention: 89%',
                      '6-month follow-up completion: 78%',
                    ],
                  ),
                  _buildBreakdownItem(
                    context,
                    'Data Quality',
                    Icons.description_rounded,
                    PremiumIcon.techGradient,
                    breakdown.dataQuality,
                    10,
                    [
                      'Session notes: 98% complete',
                      'Outcome measures: 95% compliance',
                      'Structured data entries',
                    ],
                  ),
                  _buildBreakdownItem(
                    context,
                    'Client Satisfaction',
                    Icons.star_rounded,
                    PremiumIcon.vitalityGradient,
                    breakdown.clientSatisfaction,
                    10,
                    [
                      '${practitioner.rating}/5 star rating (${practitioner.reviewCount} reviews)',
                      '92% rebooking rate',
                      '45% referral rate',
                    ],
                  ),
                  const SizedBox(height: 24),

                  // Specialty Outcome Data
                  Text(
                    'Condition-Specific Outcomes',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Column(
                        children: [
                          SizedBox(
                            height: 250,
                            child: BarChart(
                              BarChartData(
                                alignment: BarChartAlignment.spaceAround,
                                maxY: 100,
                                barTouchData: BarTouchData(enabled: false),
                                titlesData: FlTitlesData(
                                  show: true,
                                  bottomTitles: AxisTitles(
                                    sideTitles: SideTitles(
                                      showTitles: true,
                                      reservedSize: 80,
                                      getTitlesWidget: (value, meta) {
                                        final outcomes = DummyData.outcomeData;
                                        if (value.toInt() >= 0 && value.toInt() < outcomes.length) {
                                          return Padding(
                                            padding: const EdgeInsets.only(top: 8.0),
                                            child: SizedBox(
                                              width: 60,
                                              child: Text(
                                                outcomes[value.toInt()].condition,
                                                style: const TextStyle(
                                                  fontSize: 10,
                                                  color: AppTheme.textSecondary,
                                                ),
                                                textAlign: TextAlign.center,
                                              ),
                                            ),
                                          );
                                        }
                                        return const SizedBox();
                                      },
                                    ),
                                  ),
                                  leftTitles: AxisTitles(
                                    sideTitles: SideTitles(
                                      showTitles: true,
                                      reservedSize: 40,
                                      interval: 20,
                                      getTitlesWidget: (value, meta) {
                                        return Text(
                                          '${value.toInt()}%',
                                          style: const TextStyle(
                                            fontSize: 10,
                                            color: AppTheme.textLight,
                                          ),
                                        );
                                      },
                                    ),
                                  ),
                                  topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                                  rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                                ),
                                gridData: FlGridData(
                                  show: true,
                                  drawVerticalLine: false,
                                  horizontalInterval: 20,
                                  getDrawingHorizontalLine: (value) {
                                    return FlLine(
                                      color: AppTheme.warmNeutral,
                                      strokeWidth: 1,
                                    );
                                  },
                                ),
                                borderData: FlBorderData(show: false),
                                barGroups: DummyData.outcomeData.asMap().entries.map((entry) {
                                  return BarChartGroupData(
                                    x: entry.key,
                                    barRods: [
                                      BarChartRodData(
                                        toY: entry.value.improvement,
                                        color: AppTheme.primaryGreen,
                                        width: 24,
                                        borderRadius: const BorderRadius.vertical(top: Radius.circular(6)),
                                      ),
                                    ],
                                  );
                                }).toList(),
                              ),
                            ),
                          ),
                          const SizedBox(height: 16),
                          ...DummyData.outcomeData.map((outcome) {
                            return Padding(
                              padding: const EdgeInsets.symmetric(vertical: 4.0),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    outcome.condition,
                                    style: Theme.of(context).textTheme.bodySmall,
                                  ),
                                  Text(
                                    '${outcome.improvement.toStringAsFixed(0)}% (${outcome.clientCount} clients)',
                                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                          color: AppTheme.primaryGreen,
                                          fontWeight: FontWeight.w600,
                                        ),
                                  ),
                                ],
                              ),
                            );
                          }),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Treatment Modalities
                  Text(
                    'Treatment Modalities',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  GlassmorphicCard(
                    padding: const EdgeInsets.all(14.0),
                    child: Column(
                      children: [
                        _buildModalityItem(context, 'Herbal Medicine', true),
                        _buildModalityItem(context, 'Nutritional Counseling', false),
                        _buildModalityItem(context, 'Lifestyle Modifications', false),
                        _buildModalityItem(context, 'Stress Management', false),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Reviews Section
                  Text(
                    'Client Reviews',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  GlassmorphicCard(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              practitioner.rating.toString(),
                              style: Theme.of(context).textTheme.displaySmall?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: AppTheme.primaryGreen,
                                  ),
                            ),
                            const SizedBox(width: 10),
                            PremiumStarRating(
                              rating: practitioner.rating,
                              size: 22,
                            ),
                          ],
                        ),
                        const SizedBox(height: 6),
                        Text(
                          'Based on ${practitioner.reviewCount} reviews',
                          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                fontSize: 11,
                              ),
                        ),
                        const SizedBox(height: 14),
                        _buildReviewBar(context, 5, 0.75),
                        _buildReviewBar(context, 4, 0.18),
                        _buildReviewBar(context, 3, 0.05),
                        _buildReviewBar(context, 2, 0.02),
                        _buildReviewBar(context, 1, 0.00),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Book Button
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {},
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: const Text(
                        'Book Appointment',
                        style: TextStyle(fontSize: 16),
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBreakdownItem(
    BuildContext context,
    String title,
    IconData icon,
    List<Color> gradientColors,
    double score,
    int maxScore,
    List<String> details,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      child: GlassmorphicCard(
        padding: EdgeInsets.zero,
        child: Theme(
          data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
          child: ExpansionTile(
            tilePadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
            childrenPadding: const EdgeInsets.fromLTRB(14, 0, 14, 14),
            leading: PremiumIcon(
              icon: icon,
              gradientColors: gradientColors,
              size: 40,
              iconSize: 20,
              borderRadius: 12,
            ),
            title: Text(
              title,
              style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    fontSize: 13,
                  ),
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 6),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: score / maxScore,
                    minHeight: 6,
                    backgroundColor: AppTheme.warmNeutral,
                    valueColor: AlwaysStoppedAnimation<Color>(gradientColors.first),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '${score.toStringAsFixed(0)} / $maxScore pts',
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        fontSize: 10,
                      ),
                ),
              ],
            ),
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: details.map((detail) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 3.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(Icons.check_circle_rounded,
                          color: gradientColors.first,
                          size: 14,
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            detail,
                            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                  fontSize: 11,
                                ),
                          ),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildModalityItem(BuildContext context, String modality, bool isPrimary) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          PremiumIcon(
            icon: Icons.spa_rounded,
            gradientColors: isPrimary ? PremiumIcon.healingGradient : PremiumIcon.sageGradient,
            size: 28,
            iconSize: 14,
            borderRadius: 8,
            hasShadow: false,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              modality,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    fontWeight: isPrimary ? FontWeight.w600 : FontWeight.normal,
                  ),
            ),
          ),
          if (isPrimary)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: PremiumIcon.vitalityGradient,
                ),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.star_rounded, color: Colors.white, size: 12),
                  const SizedBox(width: 4),
                  Text(
                    'Primary',
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                          fontSize: 10,
                        ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildReviewBar(BuildContext context, int stars, double percentage) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3.0),
      child: Row(
        children: [
          SizedBox(
            width: 40,
            child: Row(
              children: [
                Text(
                  '$stars',
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        fontSize: 11,
                        fontWeight: FontWeight.w500,
                      ),
                ),
                const SizedBox(width: 2),
                const Icon(Icons.star_rounded, color: Color(0xFFF59E0B), size: 12),
              ],
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(3),
              child: LinearProgressIndicator(
                value: percentage,
                minHeight: 6,
                backgroundColor: AppTheme.warmNeutral,
                valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFF59E0B)),
              ),
            ),
          ),
          const SizedBox(width: 8),
          SizedBox(
            width: 32,
            child: Text(
              '${(percentage * 100).toInt()}%',
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    fontSize: 10,
                  ),
              textAlign: TextAlign.right,
            ),
          ),
        ],
      ),
    );
  }
}
