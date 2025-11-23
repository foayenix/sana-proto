import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../theme/app_theme.dart';
import '../models/dummy_data.dart';

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
                    CircleAvatar(
                      radius: 50,
                      backgroundImage: NetworkImage(practitioner.imageUrl),
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
                  Card(
                    color: AppTheme.primaryGreen,
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              const Icon(Icons.verified, color: Colors.white, size: 32),
                              const SizedBox(width: 12),
                              const Text(
                                'SANA Index Score',
                                style: TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.baseline,
                            textBaseline: TextBaseline.alphabetic,
                            children: [
                              Text(
                                practitioner.sanaIndex.toStringAsFixed(0),
                                style: const TextStyle(
                                  fontSize: 72,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                              ),
                              const Text(
                                '/100',
                                style: TextStyle(
                                  fontSize: 32,
                                  fontWeight: FontWeight.normal,
                                  color: Colors.white70,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: const Text(
                              '🏆 Top 10% of Herbalists on SANA',
                              style: TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.w600,
                              ),
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
                    '✅ Verified Credentials',
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
                    '📊 Treatment Volume',
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
                    '📈 Measured Outcomes',
                    breakdown.measuredOutcomes,
                    40,
                    [
                      'Average improvement: 42%',
                      'Effect size: 0.68 (medium-large)',
                      'Client retention: 78%',
                      '6-month follow-up completion: 72%',
                    ],
                  ),
                  _buildBreakdownItem(
                    context,
                    '📝 Data Quality',
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
                    '⭐ Client Satisfaction',
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
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          _buildModalityItem(context, 'Herbal Medicine', '⭐ Primary'),
                          _buildModalityItem(context, 'Nutritional Counseling', ''),
                          _buildModalityItem(context, 'Lifestyle Modifications', ''),
                          _buildModalityItem(context, 'Stress Management Techniques', ''),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Reviews Section
                  Text(
                    'Client Reviews',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                practitioner.rating.toString(),
                                style: Theme.of(context).textTheme.displayMedium?.copyWith(
                                      fontWeight: FontWeight.bold,
                                      color: AppTheme.primaryGreen,
                                    ),
                              ),
                              const SizedBox(width: 8),
                              const Text('⭐', style: TextStyle(fontSize: 32)),
                            ],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Based on ${practitioner.reviewCount} reviews',
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                          const SizedBox(height: 16),
                          _buildReviewBar(context, 5, 0.75),
                          _buildReviewBar(context, 4, 0.18),
                          _buildReviewBar(context, 3, 0.05),
                          _buildReviewBar(context, 2, 0.02),
                          _buildReviewBar(context, 1, 0.00),
                        ],
                      ),
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
    double score,
    int maxScore,
    List<String> details,
  ) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Theme(
        data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          leading: Container(
            width: 50,
            height: 50,
            decoration: BoxDecoration(
              color: AppTheme.primaryGreen.withOpacity(0.1),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Center(
              child: Text(
                '${score.toStringAsFixed(0)}',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      color: AppTheme.primaryGreen,
                      fontWeight: FontWeight.bold,
                    ),
              ),
            ),
          ),
          title: Text(
            title,
            style: Theme.of(context).textTheme.titleSmall,
          ),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 8),
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: score / maxScore,
                  minHeight: 8,
                  backgroundColor: AppTheme.warmNeutral,
                  valueColor: const AlwaysStoppedAnimation<Color>(AppTheme.primaryGreen),
                ),
              ),
              const SizedBox(height: 4),
              Text(
                '$score / $maxScore points',
                style: Theme.of(context).textTheme.labelSmall,
              ),
            ],
          ),
          children: [
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: details.map((detail) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('• ', style: TextStyle(color: AppTheme.primaryGreen)),
                        Expanded(
                          child: Text(
                            detail,
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModalityItem(BuildContext context, String modality, String badge) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          const Icon(Icons.check_circle, color: AppTheme.primaryGreen, size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              modality,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
          if (badge.isNotEmpty)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: AppTheme.successGreen.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                badge,
                style: Theme.of(context).textTheme.labelSmall?.copyWith(
                      color: AppTheme.successGreen,
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildReviewBar(BuildContext context, int stars, double percentage) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        children: [
          Text(
            '$stars ⭐',
            style: Theme.of(context).textTheme.labelSmall,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: percentage,
                minHeight: 8,
                backgroundColor: AppTheme.warmNeutral,
                valueColor: const AlwaysStoppedAnimation<Color>(AppTheme.primaryGreen),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Text(
            '${(percentage * 100).toInt()}%',
            style: Theme.of(context).textTheme.labelSmall,
          ),
        ],
      ),
    );
  }
}
