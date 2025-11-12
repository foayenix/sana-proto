import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ResearchPortalScreen extends StatelessWidget {
  const ResearchPortalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.lightCream,
      appBar: AppBar(
        title: const Text('Research Portal'),
        backgroundColor: AppTheme.secondaryBlue,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
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
                  const Icon(Icons.science, color: Colors.white, size: 48),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Institutional Research Access',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 4),
                        const Text(
                          'University of Westminster',
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

            // Dataset Explorer
            Text(
              'Available Datasets',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            _buildDatasetCard(
              context,
              title: 'Herbal Medicine for Anxiety',
              patients: 4500,
              sessions: 23000,
              completeness: 89,
              icon: Icons.spa,
              color: AppTheme.primaryGreen,
            ),
            _buildDatasetCard(
              context,
              title: 'Acupuncture for Chronic Pain',
              patients: 3200,
              sessions: 18000,
              completeness: 85,
              icon: Icons.healing,
              color: AppTheme.accentTeal,
            ),
            _buildDatasetCard(
              context,
              title: 'Mind-Body Therapies for Depression',
              patients: 2800,
              sessions: 15600,
              completeness: 91,
              icon: Icons.psychology,
              color: AppTheme.secondaryBlue,
            ),
            const SizedBox(height: 24),

            // Query Builder
            Text(
              'Query Builder',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.filter_list, color: AppTheme.secondaryBlue),
                        const SizedBox(width: 12),
                        Text(
                          'Build Custom Query',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    _buildQueryFilter('Condition', 'Anxiety'),
                    _buildQueryFilter('Treatment Type', 'Herbal Medicine'),
                    _buildQueryFilter('Gender', 'Female'),
                    _buildQueryFilter('Age Range', '25-45'),
                    _buildQueryFilter('Treatment Duration', '3+ months'),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppTheme.successGreen.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppTheme.successGreen.withOpacity(0.3)),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.check_circle, color: AppTheme.successGreen),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Query Results',
                                  style: Theme.of(context).textTheme.titleSmall,
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  '1,234 matching patients',
                                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                        color: AppTheme.successGreen,
                                        fontWeight: FontWeight.w600,
                                      ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.download),
                        label: const Text('Export Dataset'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.secondaryBlue,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Data Quality Indicators
            Text(
              'Data Quality Indicators',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _buildQualityCard(
                    context,
                    'Outcome Completion',
                    '89%',
                    Icons.assessment,
                    AppTheme.primaryGreen,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildQualityCard(
                    context,
                    'Follow-up Rate',
                    '76%',
                    Icons.update,
                    AppTheme.secondaryBlue,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _buildQualityCard(
                    context,
                    'Completeness',
                    '8.5/10',
                    Icons.checklist,
                    AppTheme.accentTeal,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildQualityCard(
                    context,
                    'Taxonomy Compliance',
                    '94%',
                    Icons.category,
                    AppTheme.successGreen,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Export Options
            Text(
              'Export Options',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    _buildExportOption(
                      context,
                      'CSV Format',
                      'Standard comma-separated values',
                      Icons.table_chart,
                    ),
                    _buildExportOption(
                      context,
                      'FHIR Format',
                      'HL7 Fast Healthcare Interoperability Resources',
                      Icons.medical_information,
                    ),
                    _buildExportOption(
                      context,
                      'REDCap Compatible',
                      'Research Electronic Data Capture format',
                      Icons.science,
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: AppTheme.infoBlue.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.security, size: 20, color: AppTheme.infoBlue),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              'GDPR Article 89 Compliant - All data anonymized',
                              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                    color: AppTheme.infoBlue,
                                  ),
                            ),
                          ),
                          const Icon(Icons.verified, size: 20, color: AppTheme.successGreen),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Published Research
            Text(
              'Published Research Using SANA Data',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            _buildPublicationCard(
              context,
              title: 'Efficacy of Herbal Medicine in Anxiety Disorders: A Real-World Evidence Study',
              journal: 'Journal of Complementary Medicine',
              year: '2024',
              citations: 45,
            ),
            _buildPublicationCard(
              context,
              title: 'Machine Learning Approaches to Predicting Treatment Outcomes in CAM',
              journal: 'BMC Complementary Medicine and Therapies',
              year: '2024',
              citations: 32,
            ),
            _buildPublicationCard(
              context,
              title: 'The SANA Index: A Novel Quality Metric for CAM Practitioners',
              journal: 'Evidence-Based Complementary and Alternative Medicine',
              year: '2023',
              citations: 78,
            ),
            const SizedBox(height: 24),

            // Collaboration
            Card(
              color: AppTheme.secondaryBlue.withOpacity(0.1),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.handshake, color: AppTheme.secondaryBlue, size: 32),
                        const SizedBox(width: 12),
                        Text(
                          'Collaboration Opportunities',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Interested in conducting research with SANA data? Contact our research team to discuss partnership opportunities.',
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.email),
                      label: const Text('Contact Research Team'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.secondaryBlue,
                      ),
                    ),
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

  Widget _buildDatasetCard(
    BuildContext context, {
    required String title,
    required int patients,
    required int sessions,
    required int completeness,
    required IconData icon,
    required Color color,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  width: 50,
                  height: 50,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(icon, color: color, size: 28),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '$patients patients • $sessions sessions',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Data Completeness',
                        style: Theme.of(context).textTheme.labelSmall,
                      ),
                      const SizedBox(height: 4),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(4),
                        child: LinearProgressIndicator(
                          value: completeness / 100,
                          minHeight: 8,
                          backgroundColor: AppTheme.warmNeutral,
                          valueColor: AlwaysStoppedAnimation<Color>(color),
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        '$completeness%',
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: color,
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 16),
                ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: color,
                  ),
                  child: const Text('Explore'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQueryFilter(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: const TextStyle(fontSize: 13, color: AppTheme.textSecondary),
            ),
          ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: AppTheme.warmNeutral.withOpacity(0.3),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                value,
                style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQualityCard(BuildContext context, String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: Theme.of(context).textTheme.bodySmall,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildExportOption(BuildContext context, String title, String description, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(icon, color: AppTheme.secondaryBlue),
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
                  description,
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ),
          Radio(
            value: true,
            groupValue: false,
            onChanged: (value) {},
            activeColor: AppTheme.secondaryBlue,
          ),
        ],
      ),
    );
  }

  Widget _buildPublicationCard(
    BuildContext context, {
    required String title,
    required String journal,
    required String year,
    required int citations,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Icon(Icons.book, size: 16, color: AppTheme.textSecondary),
                const SizedBox(width: 4),
                Text(
                  journal,
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  year,
                  style: Theme.of(context).textTheme.labelSmall,
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppTheme.secondaryBlue.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    '$citations citations',
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          color: AppTheme.secondaryBlue,
                          fontWeight: FontWeight.w600,
                        ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
