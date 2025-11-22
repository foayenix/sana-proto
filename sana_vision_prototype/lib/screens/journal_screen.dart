import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../theme/app_theme.dart';
import '../models/dummy_data.dart';
import '../widgets/premium_icons.dart';

class JournalScreen extends StatefulWidget {
  const JournalScreen({super.key});

  @override
  State<JournalScreen> createState() => _JournalScreenState();
}

class _JournalScreenState extends State<JournalScreen> {
  int _selectedPersonaIndex = 0;
  final TextEditingController _journalController = TextEditingController();
  bool _showResponse = false;

  @override
  void initState() {
    super.initState();
    _journalController.text = 'Feeling anxious about work presentation tomorrow';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.lightCream,
      appBar: AppBar(
        title: const Text('AI Journal (SIRM)'),
        backgroundColor: AppTheme.lightCream,
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () {
              _showJournalHistory(context);
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Info Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppTheme.infoBlue.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.infoBlue.withOpacity(0.3)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.lightbulb_outline, color: AppTheme.infoBlue),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'SIRM (SANA Insight & Reflection Model) provides personalized AI responses based on your chosen persona.',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                            color: AppTheme.infoBlue,
                          ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Journal Input
            Text(
              'How are you feeling today?',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _journalController,
              maxLines: 6,
              decoration: const InputDecoration(
                hintText: 'Share your thoughts and feelings...',
              ),
            ),
            const SizedBox(height: 24),

            // AI Persona Selector
            Text(
              'Choose Your AI Companion',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 12),
            SizedBox(
              height: 140,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: DummyData.aiPersonas.length,
                itemBuilder: (context, index) {
                  final persona = DummyData.aiPersonas[index];
                  final isSelected = _selectedPersonaIndex == index;

                  return GestureDetector(
                    onTap: () {
                      setState(() {
                        _selectedPersonaIndex = index;
                        _showResponse = false;
                      });
                    },
                    child: Container(
                      width: 120,
                      margin: const EdgeInsets.only(right: 12),
                      decoration: BoxDecoration(
                        color: isSelected ? persona.color.withOpacity(0.2) : Colors.white,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isSelected ? persona.color : Colors.transparent,
                          width: 2,
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.05),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          PremiumPersonaBadge(
                            personaId: persona.name,
                            size: 44,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            persona.name,
                            textAlign: TextAlign.center,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: Theme.of(context).textTheme.labelMedium?.copyWith(
                                  fontWeight: FontWeight.w600,
                                  fontSize: 11,
                                ),
                          ),
                          const SizedBox(height: 4),
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 4.0),
                            child: Text(
                              persona.description,
                              textAlign: TextAlign.center,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                    fontSize: 9,
                                  ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 24),

            // Get Insight Button
            Center(
              child: ElevatedButton.icon(
                onPressed: () {
                  setState(() {
                    _showResponse = true;
                  });
                },
                icon: const Icon(Icons.psychology),
                label: const Text('Get Insight'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                ),
              ),
            ),
            const SizedBox(height: 24),

            // AI Response
            if (_showResponse) ...[
              Text(
                'AI Response',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 12),
              GlassmorphicCard(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        PremiumPersonaBadge(
                          personaId: DummyData.aiPersonas[_selectedPersonaIndex].name,
                          size: 40,
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                DummyData.aiPersonas[_selectedPersonaIndex].name,
                                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.w600,
                                    ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                'AI Companion',
                                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                      color: AppTheme.textLight,
                                    ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Text(
                      DummyData.sampleAIResponses[DummyData.aiPersonas[_selectedPersonaIndex].name] ?? '',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            height: 1.6,
                          ),
                    ),
                    const SizedBox(height: 16),
                    Divider(color: AppTheme.textLight.withOpacity(0.2)),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        const Icon(Icons.insights, size: 16, color: AppTheme.textSecondary),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            'Connected to your wellness data: Your anxiety score has been elevated this week',
                            style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                  fontStyle: FontStyle.italic,
                                ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Compare All Personas
              TextButton.icon(
                onPressed: () {
                  _showAllPersonaResponses(context);
                },
                icon: const Icon(Icons.compare_arrows),
                label: const Text('Compare All Persona Responses'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  void _showAllPersonaResponses(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) {
        return DraggableScrollableSheet(
          initialChildSize: 0.9,
          minChildSize: 0.5,
          maxChildSize: 0.95,
          builder: (context, scrollController) {
            return Container(
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
              ),
              child: Column(
                children: [
                  Container(
                    margin: const EdgeInsets.symmetric(vertical: 12),
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: AppTheme.textLight,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Text(
                      'Compare All Persona Responses',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ),
                  Expanded(
                    child: ListView.builder(
                      controller: scrollController,
                      padding: const EdgeInsets.all(16.0),
                      itemCount: DummyData.aiPersonas.length,
                      itemBuilder: (context, index) {
                        final persona = DummyData.aiPersonas[index];
                        return Container(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: GlassmorphicCard(
                            padding: const EdgeInsets.all(14.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    PremiumPersonaBadge(
                                      personaId: persona.name,
                                      size: 32,
                                    ),
                                    const SizedBox(width: 10),
                                    Expanded(
                                      child: Text(
                                        persona.name,
                                        style: Theme.of(context).textTheme.titleSmall?.copyWith(
                                              fontWeight: FontWeight.w600,
                                            ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),
                                Text(
                                  DummyData.sampleAIResponses[persona.name] ?? '',
                                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                        height: 1.5,
                                      ),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  void _showJournalHistory(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) {
        return DraggableScrollableSheet(
          initialChildSize: 0.9,
          minChildSize: 0.5,
          maxChildSize: 0.95,
          builder: (context, scrollController) {
            return Container(
              decoration: const BoxDecoration(
                color: AppTheme.lightCream,
                borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
              ),
              child: Column(
                children: [
                  Container(
                    margin: const EdgeInsets.symmetric(vertical: 12),
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: AppTheme.textLight,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Journal History',
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                        IconButton(
                          icon: const Icon(Icons.close),
                          onPressed: () => Navigator.pop(context),
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: ListView.builder(
                      controller: scrollController,
                      padding: const EdgeInsets.all(16.0),
                      itemCount: DummyData.journalEntries.length,
                      itemBuilder: (context, index) {
                        final entry = DummyData.journalEntries[index];
                        return Container(
                          margin: const EdgeInsets.only(bottom: 10),
                          child: GlassmorphicCard(
                            padding: const EdgeInsets.all(14.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      DateFormat('EEE, MMM d').format(entry.date),
                                      style: Theme.of(context).textTheme.titleSmall?.copyWith(
                                            fontSize: 12,
                                          ),
                                    ),
                                    PremiumMoodIcon(
                                      mood: _emojiToMood(entry.mood),
                                      size: 28,
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),
                                Text(
                                  entry.content,
                                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                        height: 1.4,
                                      ),
                                  maxLines: 3,
                                  overflow: TextOverflow.ellipsis,
                                ),
                                const SizedBox(height: 10),
                                Wrap(
                                  spacing: 6,
                                  runSpacing: 4,
                                  children: entry.tags.map((tag) {
                                    return Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: AppTheme.warmNeutral,
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                      child: Text(
                                        tag,
                                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                                              fontSize: 10,
                                            ),
                                      ),
                                    );
                                  }).toList(),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  String _emojiToMood(String emoji) {
    switch (emoji) {
      case '😊':
      case '😄':
        return 'happy';
      case '😌':
      case '🧘':
        return 'calm';
      case '😴':
      case '💤':
        return 'tired';
      case '😰':
      case '😟':
        return 'anxious';
      case '😢':
      case '😔':
        return 'sad';
      case '⚡':
      case '💪':
        return 'energetic';
      default:
        return 'calm';
    }
  }

  @override
  void dispose() {
    _journalController.dispose();
    super.dispose();
  }
}
