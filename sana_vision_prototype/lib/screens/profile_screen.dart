import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'evidence_dashboard_screen.dart';
import 'research_portal_screen.dart';
import 'enterprise_dashboard_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.lightCream,
      appBar: AppBar(
        title: const Text('Profile & Settings'),
        backgroundColor: AppTheme.lightCream,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // User Profile Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Row(
                  children: [
                    const CircleAvatar(
                      radius: 46,
                      child: Icon(Icons.person, size: 46),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Alex Thompson',
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'alex.thompson@email.com',
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                          const SizedBox(height: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: AppTheme.primaryGreen.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              'Member since 2023',
                              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                    color: AppTheme.primaryGreen,
                                  ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.edit),
                      onPressed: () {},
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Demo Portals Section
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppTheme.accentTeal.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.accentTeal.withOpacity(0.3)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.rocket_launch, color: AppTheme.accentTeal),
                      const SizedBox(width: 12),
                      Text(
                        'SANA Vision Portals',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              color: AppTheme.accentTeal,
                            ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Explore SANA\'s future features for different user types',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: AppTheme.textSecondary,
                        ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),

            // Evidence Dashboard (Practitioner)
            _buildPortalCard(
              context,
              icon: Icons.analytics,
              title: 'Evidence Dashboard',
              subtitle: 'Practitioner Analytics & Insights',
              color: AppTheme.primaryGreen,
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const EvidenceDashboardScreen()),
                );
              },
            ),

            // Research Portal (Institutional)
            _buildPortalCard(
              context,
              icon: Icons.science,
              title: 'Research Portal',
              subtitle: 'Institutional Access & Data Explorer',
              color: AppTheme.secondaryBlue,
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const ResearchPortalScreen()),
                );
              },
            ),

            // Enterprise Dashboard (NHS/Corporate)
            _buildPortalCard(
              context,
              icon: Icons.business,
              title: 'Enterprise Dashboard',
              subtitle: 'NHS & Corporate Integration',
              color: AppTheme.accentTeal,
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const EnterpriseDashboardScreen()),
                );
              },
            ),
            const SizedBox(height: 24),

            // Settings Sections
            Text(
              'Account Settings',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _buildSettingsItem(context, Icons.person, 'Personal Information', () {}),
            _buildSettingsItem(context, Icons.lock, 'Privacy & Security', () {}),
            _buildSettingsItem(context, Icons.notifications, 'Notifications', () {}),
            const SizedBox(height: 24),

            Text(
              'Integrations',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _buildIntegrationItem(context, '🍎 Apple Health', true),
            _buildIntegrationItem(context, '⌚ Oura Ring', true),
            _buildIntegrationItem(context, '📱 Fitbit', false),
            _buildIntegrationItem(context, '💪 WHOOP', false),
            const SizedBox(height: 24),

            Text(
              'Support',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _buildSettingsItem(context, Icons.help_outline, 'Help Center', () {}),
            _buildSettingsItem(context, Icons.feedback, 'Send Feedback', () {}),
            _buildSettingsItem(context, Icons.info_outline, 'About SANA', () {}),
            const SizedBox(height: 24),

            // Logout Button
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.logout),
                label: const Text('Log Out'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: AppTheme.errorRed,
                  side: const BorderSide(color: AppTheme.errorRed),
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildPortalCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
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
                      subtitle,
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: AppTheme.textLight),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSettingsItem(BuildContext context, IconData icon, String title, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: AppTheme.primaryGreen),
        title: Text(title),
        trailing: const Icon(Icons.chevron_right, color: AppTheme.textLight),
        onTap: onTap,
      ),
    );
  }

  Widget _buildIntegrationItem(BuildContext context, String title, bool connected) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        title: Text(title),
        trailing: Switch(
          value: connected,
          onChanged: (value) {},
          activeColor: AppTheme.primaryGreen,
        ),
      ),
    );
  }
}
