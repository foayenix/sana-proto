import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../theme/app_theme.dart';
import '../models/dummy_data.dart';

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
                          Text(
                            persona.emoji,
                            style: const TextStyle(fontSize: 40),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            persona.name,
                            textAlign: TextAlign.center,
                            style: Theme.of(context).textTheme.labelMedium?.copyWith(
                                  fontWeight: FontWeight.w600,
                                ),
                          ),
                          const SizedBox(height: 4),
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 8.0),
                            child: Text(
                              persona.description,
                              textAlign: TextAlign.center,
                              style: Theme.of(context).textTheme.labelSmall,
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
              Card(
                color: DummyData.aiPersonas[_selectedPersonaIndex].color.withOpacity(0.05),
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Text(
                            DummyData.aiPersonas[_selectedPersonaIndex].emoji,
                            style: const TextStyle(fontSize: 30),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              DummyData.aiPersonas[_selectedPersonaIndex].name,
                              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                    color: DummyData.aiPersonas[_selectedPersonaIndex].color,
                                  ),
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
                      Divider(color: DummyData.aiPersonas[_selectedPersonaIndex].color.withOpacity(0.3)),
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
                        return Card(
                          margin: const EdgeInsets.only(bottom: 16),
                          color: persona.color.withOpacity(0.05),
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Text(persona.emoji, style: const TextStyle(fontSize: 24)),
                                    const SizedBox(width: 12),
                                    Text(
                                      persona.name,
                                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                            color: persona.color,
                                          ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 12),
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
                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      DateFormat('EEEE, MMM d').format(entry.date),
                                      style: Theme.of(context).textTheme.titleSmall,
                                    ),
                                    Text(entry.mood, style: const TextStyle(fontSize: 24)),
                                  ],
                                ),
                                const SizedBox(height: 12),
                                Text(
                                  entry.content,
                                  style: Theme.of(context).textTheme.bodyMedium,
                                ),
                                const SizedBox(height: 12),
                                Wrap(
                                  spacing: 8,
                                  children: entry.tags.map((tag) {
                                    return Chip(
                                      label: Text(tag),
                                      labelStyle: Theme.of(context).textTheme.labelSmall,
                                      padding: const EdgeInsets.symmetric(horizontal: 8),
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

  @override
  void dispose() {
    _journalController.dispose();
    super.dispose();
  }
}
