import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../theme/app_theme.dart';

class EnterpriseDashboardScreen extends StatefulWidget {
  const EnterpriseDashboardScreen({super.key});

  @override
  State<EnterpriseDashboardScreen> createState() => _EnterpriseDashboardScreenState();
}

class _EnterpriseDashboardScreenState extends State<EnterpriseDashboardScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.lightCream,
      appBar: AppBar(
        title: const Text('Enterprise Dashboard'),
        backgroundColor: AppTheme.accentTeal,
        foregroundColor: Colors.white,
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.white,
          labelColor: Colors.white,
          tabs: const [
            Tab(text: 'NHS Integration'),
            Tab(text: 'Corporate Wellness'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildNHSTab(context),
          _buildCorporateTab(context),
        ],
      ),
    );
  }

  Widget _buildNHSTab(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Welcome Banner
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [AppTheme.accentTeal, AppTheme.primaryGreen],
              ),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              children: [
                Container(
                  width: 60,
                  height: 60,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Center(
                    child: Text(
                      'NHS',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            color: AppTheme.accentTeal,
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'NHS Social Prescribing',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'Primary Care Network Dashboard',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.white70,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Social Prescribing Overview
          Text(
            'Social Prescribing Overview',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _buildMetricCard(
                  context,
                  'Active Referrals',
                  '234',
                  Icons.person_add,
                  AppTheme.accentTeal,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildMetricCard(
                  context,
                  'Completed',
                  '156',
                  Icons.check_circle,
                  AppTheme.successGreen,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _buildMetricCard(
                  context,
                  'Pending',
                  '45',
                  Icons.schedule,
                  AppTheme.warningOrange,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildMetricCard(
                  context,
                  'GP Practices',
                  '12',
                  Icons.local_hospital,
                  AppTheme.secondaryBlue,
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),

          // Referral Flow
          Text(
            'Bi-Directional Referral Flow',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  _buildReferralStep('1', 'GP Practice', 'Patient referral sent', Colors.blue),
                  const Icon(Icons.arrow_downward, color: AppTheme.textLight),
                  _buildReferralStep('2', 'SANA Practitioner', 'Treatment provided', AppTheme.primaryGreen),
                  const Icon(Icons.arrow_downward, color: AppTheme.textLight),
                  _buildReferralStep('3', 'Outcome Data', 'Feedback to GP', AppTheme.accentTeal),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.successGreen.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.sync, color: AppTheme.successGreen),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            'Real-time integration with NHS systems',
                            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                  color: AppTheme.successGreen,
                                ),
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

          // ROI Calculator
          Text(
            'Return on Investment',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            color: AppTheme.successGreen.withOpacity(0.1),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  Row(
                    children: [
                      const Icon(Icons.savings, color: AppTheme.successGreen, size: 40),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '£124,000',
                              style: Theme.of(context).textTheme.displayMedium?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: AppTheme.successGreen,
                                  ),
                            ),
                            Text(
                              'NHS Cost Savings (12 months)',
                              style: Theme.of(context).textTheme.bodyMedium,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  _buildSavingsItem('Reduced GP visits', '£45,000'),
                  _buildSavingsItem('Reduced prescriptions', '£38,000'),
                  _buildSavingsItem('Prevented hospital admissions', '£28,000'),
                  _buildSavingsItem('Reduced A&E attendance', '£13,000'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Patient Outcomes
          Text(
            'Patient Outcomes',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildOutcomeMetric(context, 'Satisfaction', '4.6/5', '⭐'),
                      Container(width: 1, height: 40, color: AppTheme.warmNeutral),
                      _buildOutcomeMetric(context, 'Adherence', '82%', '✅'),
                      Container(width: 1, height: 40, color: AppTheme.warmNeutral),
                      _buildOutcomeMetric(context, 'Readmission', '-34%', '📉'),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Integration Status
          Text(
            'Integration Status',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  _buildIntegrationStatus('NHS App Connected', true),
                  _buildIntegrationStatus('FHIR API Active', true),
                  _buildIntegrationStatus('GP Connect Enabled', true),
                  _buildIntegrationStatus('Summary Care Record Access', true),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Map of GP Practices
          Text(
            'Connected GP Practices',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  Container(
                    height: 200,
                    decoration: BoxDecoration(
                      color: AppTheme.warmNeutral.withOpacity(0.3),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.map, size: 64, color: AppTheme.textLight),
                          const SizedBox(height: 12),
                          Text(
                            'Interactive Map',
                            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                  color: AppTheme.textSecondary,
                                ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            '12 GP practices across the region',
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  _buildPracticeItem('Riverside Medical Centre', '45 referrals'),
                  _buildPracticeItem('Greenwood Surgery', '38 referrals'),
                  _buildPracticeItem('City Health Practice', '32 referrals'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildCorporateTab(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Welcome Banner
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [AppTheme.secondaryBlue, AppTheme.accentTeal],
              ),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              children: [
                const Icon(Icons.business, color: Colors.white, size: 48),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Corporate Wellness',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'TechCorp Global - Employee Dashboard',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.white70,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Enrollment Overview
          Text(
            'Program Overview',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _buildMetricCard(
                  context,
                  'Enrolled',
                  '1,250',
                  Icons.badge,
                  AppTheme.secondaryBlue,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildMetricCard(
                  context,
                  'Active Users',
                  '890 (71%)',
                  Icons.people,
                  AppTheme.accentTeal,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _buildMetricCard(
                  context,
                  'Avg Health Score',
                  '74/100',
                  Icons.favorite,
                  AppTheme.primaryGreen,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildMetricCard(
                  context,
                  'Engagement',
                  '4.2/5',
                  Icons.star,
                  AppTheme.warningOrange,
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),

          // Company Wellness Trends
          Text(
            'Company Wellness Trends',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  SizedBox(
                    height: 200,
                    child: LineChart(
                      LineChartData(
                        gridData: FlGridData(
                          show: true,
                          drawVerticalLine: false,
                        ),
                        titlesData: FlTitlesData(
                          bottomTitles: AxisTitles(
                            sideTitles: SideTitles(
                              showTitles: true,
                              getTitlesWidget: (value, meta) {
                                final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
                                if (value.toInt() < months.length) {
                                  return Text(
                                    months[value.toInt()],
                                    style: const TextStyle(fontSize: 10),
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
                            ),
                          ),
                          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                        ),
                        borderData: FlBorderData(show: false),
                        lineBarsData: [
                          LineChartBarData(
                            spots: const [
                              FlSpot(0, 68),
                              FlSpot(1, 70),
                              FlSpot(2, 72),
                              FlSpot(3, 71),
                              FlSpot(4, 73),
                              FlSpot(5, 74),
                            ],
                            isCurved: true,
                            color: AppTheme.primaryGreen,
                            barWidth: 3,
                            dotData: const FlDotData(show: true),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Average employee wellness score has increased 9% since program launch',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: AppTheme.successGreen,
                        ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Popular Services
          Text(
            'Most Popular Services',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  SizedBox(
                    height: 200,
                    child: BarChart(
                      BarChartData(
                        alignment: BarChartAlignment.spaceAround,
                        maxY: 350,
                        barTouchData: BarTouchData(enabled: false),
                        titlesData: FlTitlesData(
                          bottomTitles: AxisTitles(
                            sideTitles: SideTitles(
                              showTitles: true,
                              getTitlesWidget: (value, meta) {
                                final services = ['Stress\nMgmt', 'Nutrition', 'Massage', 'Yoga'];
                                if (value.toInt() < services.length) {
                                  return Padding(
                                    padding: const EdgeInsets.only(top: 8.0),
                                    child: Text(
                                      services[value.toInt()],
                                      style: const TextStyle(fontSize: 10),
                                      textAlign: TextAlign.center,
                                    ),
                                  );
                                }
                                return const SizedBox();
                              },
                            ),
                          ),
                          leftTitles: AxisTitles(
                            sideTitles: SideTitles(showTitles: true, reservedSize: 40),
                          ),
                          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                        ),
                        gridData: FlGridData(show: true, drawVerticalLine: false),
                        borderData: FlBorderData(show: false),
                        barGroups: [
                          BarChartGroupData(x: 0, barRods: [
                            BarChartRodData(toY: 312, color: AppTheme.primaryGreen, width: 24)
                          ]),
                          BarChartGroupData(x: 1, barRods: [
                            BarChartRodData(toY: 267, color: AppTheme.secondaryBlue, width: 24)
                          ]),
                          BarChartGroupData(x: 2, barRods: [
                            BarChartRodData(toY: 198, color: AppTheme.accentTeal, width: 24)
                          ]),
                          BarChartGroupData(x: 3, barRods: [
                            BarChartRodData(toY: 145, color: AppTheme.warningOrange, width: 24)
                          ]),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Department Comparisons
          Text(
            'Department Wellness Comparison',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          _buildDepartmentCard('Engineering', 76, AppTheme.primaryGreen),
          _buildDepartmentCard('Sales', 72, AppTheme.secondaryBlue),
          _buildDepartmentCard('Marketing', 74, AppTheme.accentTeal),
          _buildDepartmentCard('Operations', 71, AppTheme.warningOrange),
          const SizedBox(height: 24),

          // ROI Impact
          Text(
            'Business Impact',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            color: AppTheme.successGreen.withOpacity(0.1),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  _buildImpactMetric('Reduced sick days', '18%', Icons.trending_down),
                  _buildImpactMetric('Increased productivity', '12%', Icons.trending_up),
                  _buildImpactMetric('Improved retention', '22%', Icons.people),
                  _buildImpactMetric('Employee satisfaction', '+15 NPS', Icons.sentiment_satisfied),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          // Integration Status
          Text(
            'Integration Status',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  _buildIntegrationStatus('Benefits Platform Integrated', true),
                  _buildIntegrationStatus('Single Sign-On Enabled', true),
                  _buildIntegrationStatus('HR System Connected', true),
                  _buildIntegrationStatus('Slack/Teams Integration', true),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildMetricCard(BuildContext context, String title, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 12),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildReferralStep(String number, String title, String subtitle, Color color) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
            child: Center(
              child: Text(
                number,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                ),
              ),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleSmall,
                ),
                const SizedBox(height: 2),
                Text(
                  subtitle,
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSavingsItem(String label, String amount) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 13)),
          Text(
            amount,
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: AppTheme.successGreen,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildOutcomeMetric(BuildContext context, String label, String value, String emoji) {
    return Column(
      children: [
        Text(emoji, style: const TextStyle(fontSize: 24)),
        const SizedBox(height: 8),
        Text(
          value,
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
                color: AppTheme.accentTeal,
              ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: Theme.of(context).textTheme.bodySmall,
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildIntegrationStatus(String title, bool connected) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(
            connected ? Icons.check_circle : Icons.cancel,
            color: connected ? AppTheme.successGreen : AppTheme.errorRed,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              title,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: (connected ? AppTheme.successGreen : AppTheme.errorRed).withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              connected ? 'Active' : 'Inactive',
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    color: connected ? AppTheme.successGreen : AppTheme.errorRed,
                    fontWeight: FontWeight.w600,
                  ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPracticeItem(String name, String referrals) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          const Icon(Icons.location_on, size: 20, color: AppTheme.accentTeal),
          const SizedBox(width: 12),
          Expanded(
            child: Text(name, style: const TextStyle(fontSize: 13)),
          ),
          Text(
            referrals,
            style: const TextStyle(
              fontSize: 12,
              color: AppTheme.textSecondary,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDepartmentCard(String department, int score, Color color) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Expanded(
              child: Text(
                department,
                style: Theme.of(context).textTheme.titleSmall,
              ),
            ),
            Text(
              '$score/100',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: color,
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(width: 12),
            SizedBox(
              width: 100,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: score / 100,
                  minHeight: 8,
                  backgroundColor: AppTheme.warmNeutral,
                  valueColor: AlwaysStoppedAnimation<Color>(color),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildImpactMetric(String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(icon, color: AppTheme.successGreen, size: 28),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              label,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
          Text(
            value,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppTheme.successGreen,
                  fontWeight: FontWeight.bold,
                ),
          ),
        ],
      ),
    );
  }
}
