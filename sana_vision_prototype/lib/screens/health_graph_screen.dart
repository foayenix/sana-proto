import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../theme/app_theme.dart';
import '../models/dummy_data.dart';
import '../widgets/score_card.dart';
import 'package:intl/intl.dart';

class HealthGraphScreen extends StatelessWidget {
  const HealthGraphScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final healthScore = DummyData.currentHealthScore;

    return Scaffold(
      backgroundColor: AppTheme.lightCream,
      appBar: AppBar(
        title: const Text('SANA Health Graph'),
        backgroundColor: AppTheme.lightCream,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Main Score Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    ScoreCard(
                      title: 'SANA Health Score',
                      score: healthScore.overall,
                      change: 3.0,
                      subtitle: healthScore.status,
                      color: AppTheme.getStatusColor(healthScore.status),
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _buildAgeComparison(
                          context,
                          'Biological Age',
                          healthScore.biologicalAge,
                          Colors.green,
                        ),
                        Container(
                          width: 1,
                          height: 40,
                          color: AppTheme.warmNeutral,
                        ),
                        _buildAgeComparison(
                          context,
                          'Chronological Age',
                          healthScore.chronologicalAge,
                          AppTheme.textSecondary,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Top 3 Levers
            Text(
              'Top 3 Levers',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(
              'AI-generated personalized recommendations',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 12),
            ...DummyData.topLevers.map((lever) => _buildLeverCard(context, lever)),
            const SizedBox(height: 24),

            // Multi-dimensional Visualization
            Text(
              '360° Wellness Dimensions',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    SizedBox(
                      height: 300,
                      child: RadarChart(
                        RadarChartData(
                          radarShape: RadarShape.polygon,
                          radarBackgroundColor: Colors.transparent,
                          radarBorderData: const BorderSide(color: AppTheme.warmNeutral, width: 2),
                          gridBorderData: const BorderSide(color: AppTheme.warmNeutral, width: 1),
                          tickBorderData: const BorderSide(color: Colors.transparent),
                          tickCount: 5,
                          ticksTextStyle: const TextStyle(fontSize: 10, color: AppTheme.textLight),
                          radarTouchData: RadarTouchData(enabled: false),
                          dataSets: [
                            RadarDataSet(
                              fillColor: AppTheme.primaryGreen.withOpacity(0.3),
                              borderColor: AppTheme.primaryGreen,
                              borderWidth: 3,
                              dataEntries: [
                                RadarEntry(value: healthScore.physical),
                                RadarEntry(value: healthScore.mental),
                                RadarEntry(value: healthScore.emotional),
                                RadarEntry(value: healthScore.social),
                                RadarEntry(value: healthScore.sleep),
                                RadarEntry(value: healthScore.energy),
                              ],
                            ),
                          ],
                          getTitle: (index, angle) {
                            final titles = [
                              'Physical\nHealth',
                              'Mental\nWellbeing',
                              'Emotional\nBalance',
                              'Social\nConnection',
                              'Sleep\nQuality',
                              'Energy\nLevels',
                            ];
                            return RadarChartTitle(text: titles[index]);
                          },
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    _buildDimensionList(context, healthScore),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Data Sources
            Text(
              'Data Sources',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: DummyData.dataSources.map((source) {
                    return Padding(
                      padding: const EdgeInsets.symmetric(vertical: 8.0),
                      child: Row(
                        children: [
                          Container(
                            width: 40,
                            height: 40,
                            decoration: BoxDecoration(
                              color: AppTheme.primaryGreen.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Icon(source.icon, color: AppTheme.primaryGreen, size: 20),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              source.name,
                              style: Theme.of(context).textTheme.bodyMedium,
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: AppTheme.primaryGreen.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(
                              '${source.count} entries',
                              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                    color: AppTheme.primaryGreen,
                                    fontWeight: FontWeight.w600,
                                  ),
                            ),
                          ),
                        ],
                      ),
                    );
                  }).toList(),
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Timeline View
            Text(
              '12-Month Timeline',
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
                      child: LineChart(
                        LineChartData(
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
                          titlesData: FlTitlesData(
                            bottomTitles: AxisTitles(
                              sideTitles: SideTitles(
                                showTitles: true,
                                reservedSize: 30,
                                interval: 1,
                                getTitlesWidget: (value, meta) {
                                  if (value.toInt() >= 0 && value.toInt() < DummyData.historicalScores.length) {
                                    final date = DummyData.historicalScores.reversed.toList()[value.toInt()].date;
                                    return Padding(
                                      padding: const EdgeInsets.only(top: 8.0),
                                      child: Text(
                                        DateFormat('MMM').format(date),
                                        style: const TextStyle(fontSize: 10, color: AppTheme.textLight),
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
                                    value.toInt().toString(),
                                    style: const TextStyle(fontSize: 10, color: AppTheme.textLight),
                                  );
                                },
                              ),
                            ),
                            topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                            rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                          ),
                          borderData: FlBorderData(show: false),
                          minY: 0,
                          maxY: 100,
                          lineBarsData: [
                            LineChartBarData(
                              spots: DummyData.historicalScores.reversed.toList().asMap().entries.map((entry) {
                                return FlSpot(entry.key.toDouble(), entry.value.score);
                              }).toList(),
                              isCurved: true,
                              color: AppTheme.primaryGreen,
                              barWidth: 3,
                              isStrokeCapRound: true,
                              dotData: FlDotData(
                                show: true,
                                getDotPainter: (spot, percent, barData, index) {
                                  final hasAnnotation = DummyData.historicalScores.reversed.toList()[index].annotation != null;
                                  return FlDotCirclePainter(
                                    radius: hasAnnotation ? 6 : 4,
                                    color: hasAnnotation ? AppTheme.accentTeal : AppTheme.primaryGreen,
                                    strokeWidth: hasAnnotation ? 2 : 0,
                                    strokeColor: Colors.white,
                                  );
                                },
                              ),
                              belowBarData: BarAreaData(
                                show: true,
                                color: AppTheme.primaryGreen.withOpacity(0.1),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    ...DummyData.historicalScores.where((s) => s.annotation != null).map((score) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Row(
                          children: [
                            Container(
                              width: 8,
                              height: 8,
                              decoration: const BoxDecoration(
                                color: AppTheme.accentTeal,
                                shape: BoxShape.circle,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              DateFormat('MMM d').format(score.date),
                              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                    fontWeight: FontWeight.w600,
                                  ),
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                score.annotation!,
                                style: Theme.of(context).textTheme.bodySmall,
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
          ],
        ),
      ),
    );
  }

  Widget _buildAgeComparison(BuildContext context, String label, int age, Color color) {
    return Column(
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.bodySmall,
        ),
        const SizedBox(height: 4),
        Text(
          '$age',
          style: Theme.of(context).textTheme.displaySmall?.copyWith(
                fontWeight: FontWeight.bold,
                color: color,
              ),
        ),
      ],
    );
  }

  Widget _buildLeverCard(BuildContext context, Lever lever) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Container(
              width: 50,
              height: 50,
              decoration: BoxDecoration(
                color: AppTheme.primaryGreen.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(lever.icon, color: AppTheme.primaryGreen),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text(
                        lever.title,
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: AppTheme.successGreen.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          lever.impact,
                          style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                color: AppTheme.successGreen,
                                fontWeight: FontWeight.w600,
                              ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(
                    lever.description,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
            IconButton(
              icon: const Icon(Icons.arrow_forward, color: AppTheme.textLight),
              onPressed: () {},
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDimensionList(BuildContext context, HealthScore healthScore) {
    final dimensions = [
      {'name': 'Physical Health', 'score': healthScore.physical, 'icon': Icons.fitness_center},
      {'name': 'Mental Wellbeing', 'score': healthScore.mental, 'icon': Icons.psychology},
      {'name': 'Emotional Balance', 'score': healthScore.emotional, 'icon': Icons.favorite},
      {'name': 'Social Connection', 'score': healthScore.social, 'icon': Icons.people},
      {'name': 'Sleep Quality', 'score': healthScore.sleep, 'icon': Icons.bedtime},
      {'name': 'Energy Levels', 'score': healthScore.energy, 'icon': Icons.bolt},
    ];

    return Column(
      children: dimensions.map((dim) {
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0),
          child: Row(
            children: [
              Icon(dim['icon'] as IconData, size: 20, color: AppTheme.primaryGreen),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  dim['name'] as String,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
              Text(
                '${(dim['score'] as double).toStringAsFixed(0)}/100',
                style: Theme.of(context).textTheme.titleSmall?.copyWith(
                      color: AppTheme.primaryGreen,
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}
