import 'package:flutter/material.dart';

class HealthScore {
  final double overall;
  final double physical;
  final double mental;
  final double emotional;
  final double social;
  final double sleep;
  final double energy;
  final String status;
  final int biologicalAge;
  final int chronologicalAge;

  HealthScore({
    required this.overall,
    required this.physical,
    required this.mental,
    required this.emotional,
    required this.social,
    required this.sleep,
    required this.energy,
    required this.status,
    required this.biologicalAge,
    required this.chronologicalAge,
  });
}

class Lever {
  final String title;
  final String description;
  final IconData icon;
  final String impact;

  Lever({
    required this.title,
    required this.description,
    required this.icon,
    required this.impact,
  });
}

class DataSource {
  final String name;
  final int count;
  final IconData icon;

  DataSource({required this.name, required this.count, required this.icon});
}

class HistoricalScore {
  final DateTime date;
  final double score;
  final String? annotation;

  HistoricalScore({required this.date, required this.score, this.annotation});
}

class JournalEntry {
  final DateTime date;
  final String content;
  final String mood;
  final List<String> tags;

  JournalEntry({
    required this.date,
    required this.content,
    required this.mood,
    required this.tags,
  });
}

class AIPersona {
  final String name;
  final String emoji;
  final String description;
  final Color color;

  AIPersona({
    required this.name,
    required this.emoji,
    required this.description,
    required this.color,
  });
}

class AIResponse {
  final String persona;
  final String response;

  AIResponse({required this.persona, required this.response});
}

class Practitioner {
  final String name;
  final String title;
  final String specialty;
  final double sanaIndex;
  final String imageUrl;
  final int yearsExperience;
  final int clientsGraduated;
  final int totalSessions;
  final double rating;
  final int reviewCount;

  Practitioner({
    required this.name,
    required this.title,
    required this.specialty,
    required this.sanaIndex,
    required this.imageUrl,
    required this.yearsExperience,
    required this.clientsGraduated,
    required this.totalSessions,
    required this.rating,
    required this.reviewCount,
  });
}

class SanaIndexBreakdown {
  final double credentials;
  final double treatmentVolume;
  final double measuredOutcomes;
  final double dataQuality;
  final double clientSatisfaction;

  SanaIndexBreakdown({
    required this.credentials,
    required this.treatmentVolume,
    required this.measuredOutcomes,
    required this.dataQuality,
    required this.clientSatisfaction,
  });
}

class OutcomeData {
  final String condition;
  final double improvement;
  final int clientCount;

  OutcomeData({
    required this.condition,
    required this.improvement,
    required this.clientCount,
  });
}

class Appointment {
  final DateTime dateTime;
  final Practitioner practitioner;
  final String type;
  final String status;

  Appointment({
    required this.dateTime,
    required this.practitioner,
    required this.type,
    required this.status,
  });
}

class ActivityItem {
  final String title;
  final String description;
  final DateTime timestamp;
  final IconData icon;
  final Color color;

  ActivityItem({
    required this.title,
    required this.description,
    required this.timestamp,
    required this.icon,
    required this.color,
  });
}

class WearableData {
  final String name;
  final String value;
  final IconData icon;

  WearableData({required this.name, required this.value, required this.icon});
}

class DummyData {
  // Current Health Score
  static final HealthScore currentHealthScore = HealthScore(
    overall: 78.0,
    physical: 85.0,
    mental: 72.0,
    emotional: 90.0,
    social: 68.0,
    sleep: 78.0,
    energy: 82.0,
    status: 'Thriving',
    biologicalAge: 32,
    chronologicalAge: 38,
  );

  // Top 3 Levers
  static final List<Lever> topLevers = [
    Lever(
      title: 'Morning Meditation',
      description: 'Adding 10 minutes of meditation could improve your mental wellbeing score by 8 points',
      icon: Icons.self_improvement,
      impact: '+8 points',
    ),
    Lever(
      title: 'Social Connection',
      description: 'Schedule 2 social activities this week to boost your connection score',
      icon: Icons.people,
      impact: '+6 points',
    ),
    Lever(
      title: 'Sleep Consistency',
      description: 'Maintaining consistent sleep schedule could improve overall score by 5 points',
      icon: Icons.bedtime,
      impact: '+5 points',
    ),
  ];

  // Data Sources
  static final List<DataSource> dataSources = [
    DataSource(name: 'Practitioner Sessions', count: 15, icon: Icons.medical_services),
    DataSource(name: 'Self-Reported Symptoms', count: 120, icon: Icons.edit_note),
    DataSource(name: 'Wearable Data', count: 365, icon: Icons.watch),
    DataSource(name: 'Journal Entries', count: 45, icon: Icons.book),
    DataSource(name: 'Lifestyle Tracking', count: 89, icon: Icons.fitness_center),
  ];

  // Historical Scores (12 months)
  static final List<HistoricalScore> historicalScores = [
    HistoricalScore(date: DateTime(2024, 11, 12), score: 78.0),
    HistoricalScore(date: DateTime(2024, 10, 12), score: 75.0),
    HistoricalScore(date: DateTime(2024, 9, 12), score: 76.0, annotation: 'Started new herbal protocol'),
    HistoricalScore(date: DateTime(2024, 8, 12), score: 72.0),
    HistoricalScore(date: DateTime(2024, 7, 12), score: 68.0),
    HistoricalScore(date: DateTime(2024, 6, 12), score: 65.0, annotation: 'Began acupuncture'),
    HistoricalScore(date: DateTime(2024, 5, 12), score: 62.0),
    HistoricalScore(date: DateTime(2024, 4, 12), score: 58.0),
    HistoricalScore(date: DateTime(2024, 3, 12), score: 55.0),
    HistoricalScore(date: DateTime(2024, 2, 12), score: 54.0),
    HistoricalScore(date: DateTime(2024, 1, 12), score: 52.0),
    HistoricalScore(date: DateTime(2023, 12, 12), score: 50.0, annotation: 'Started SANA journey'),
  ];

  // AI Personas
  static final List<AIPersona> aiPersonas = [
    AIPersona(
      name: 'Compassionate Therapist',
      emoji: '🧘',
      description: 'Empathetic, supportive',
      color: const Color(0xFF81B29A),
    ),
    AIPersona(
      name: 'Wise Philosopher',
      emoji: '📚',
      description: 'Thought-provoking, profound',
      color: const Color(0xFF7BA5C6),
    ),
    AIPersona(
      name: 'Creative Poet',
      emoji: '🎨',
      description: 'Metaphorical, artistic',
      color: const Color(0xFFF2A65A),
    ),
    AIPersona(
      name: 'Evidence-Based Coach',
      emoji: '🔬',
      description: 'Practical, research-backed',
      color: const Color(0xFF5A9B9B),
    ),
  ];

  // Sample AI Responses
  static final Map<String, String> sampleAIResponses = {
    'Compassionate Therapist': 'I hear that you\'re feeling anxious about your presentation tomorrow, and that\'s completely valid. Performance anxiety is something many people experience. Your body is responding to what it perceives as a challenge.\n\nI\'ve noticed your anxiety score has been elevated this week, rising from 4/10 to 7/10. This suggests you might benefit from some grounding techniques.\n\nTry this: Take 5 deep breaths before bed tonight, inhaling for 4 counts and exhaling for 6. This activates your parasympathetic nervous system. Also, prepare your opening sentence - having that ready can reduce anticipatory anxiety by 40%.',

    'Wise Philosopher': 'The ancient Stoics taught us that we suffer more in imagination than in reality. Your anxiety about tomorrow\'s presentation exists only in the realm of possibility, not actuality.\n\nConsider: What would you tell a dear friend in this situation? Often, we extend more compassion to others than ourselves. Your elevated anxiety this week (reflected in your wellness data) suggests a pattern worth examining.\n\nPractice "premeditatio malorum" - imagine the worst outcome. You fumble words. And then? Life continues. This paradoxical technique often dissolves anxiety by revealing its disproportionate nature.',

    'Creative Poet': 'Anxiety before a presentation is like a river before a waterfall - gathering energy, building momentum, preparing to cascade. Your nervous system is composing a symphony, every instrument tuning up before the performance.\n\nYour wellness data shows this crescendo building over the week - from gentle streams to rushing rapids. But remember: waterfalls are beautiful, and so is your voice when you let it flow.\n\nTonight, write your fears on paper, then write them backwards. Let them become abstract art rather than concrete monsters. Transform the energy rather than fighting it.',

    'Evidence-Based Coach': 'Pre-performance anxiety is a normal physiological response. Your HRV data shows increased sympathetic nervous system activation this week, correlating with your self-reported anxiety scores.\n\nResearch shows these evidence-based interventions reduce presentation anxiety:\n1. Physical practice: Rehearse standing up 3 times (reduces anxiety by 31%)\n2. Power posing: 2 minutes before presenting (increases confidence by 20%)\n3. Reframing: Say "I\'m excited" instead of "I\'m nervous" (improves performance)\n\nYour historical data shows you perform well under pressure - your last presentation received positive feedback despite similar pre-event anxiety.',
  };

  // Sample Journal Entries
  static final List<JournalEntry> journalEntries = [
    JournalEntry(
      date: DateTime(2024, 11, 12),
      content: 'Feeling anxious about work presentation tomorrow',
      mood: '😰',
      tags: ['anxiety', 'work', 'stress'],
    ),
    JournalEntry(
      date: DateTime(2024, 11, 11),
      content: 'Had a wonderful day with family. Feeling grateful and energized.',
      mood: '😊',
      tags: ['gratitude', 'family', 'happiness'],
    ),
    JournalEntry(
      date: DateTime(2024, 11, 10),
      content: 'Sleep was much better last night after trying the herbal tea blend.',
      mood: '😌',
      tags: ['sleep', 'herbs', 'wellness'],
    ),
  ];

  // Featured Practitioner
  static final Practitioner featuredPractitioner = Practitioner(
    name: 'Dr. Sarah Johnson',
    title: 'BSc Herbal Medicine',
    specialty: 'Anxiety & Digestive Health',
    sanaIndex: 87.0,
    imageUrl: 'https://i.pravatar.cc/300?img=1',
    yearsExperience: 8,
    clientsGraduated: 450,
    totalSessions: 2300,
    rating: 4.8,
    reviewCount: 234,
  );

  // SANA Index Breakdown
  static final SanaIndexBreakdown sanaIndexBreakdown = SanaIndexBreakdown(
    credentials: 20.0,
    treatmentVolume: 18.0,
    measuredOutcomes: 38.0,
    dataQuality: 9.0,
    clientSatisfaction: 9.0,
  );

  // Outcome Data
  static final List<OutcomeData> outcomeData = [
    OutcomeData(condition: 'Anxiety & Stress', improvement: 78.0, clientCount: 180),
    OutcomeData(condition: 'Digestive Issues', improvement: 71.0, clientCount: 120),
    OutcomeData(condition: 'Sleep Disorders', improvement: 84.0, clientCount: 95),
    OutcomeData(condition: 'Chronic Pain', improvement: 65.0, clientCount: 55),
  ];

  // Upcoming Appointments
  static final List<Appointment> upcomingAppointments = [
    Appointment(
      dateTime: DateTime(2024, 11, 15, 14, 30),
      practitioner: featuredPractitioner,
      type: 'Follow-up Consultation',
      status: 'confirmed',
    ),
  ];

  // Recent Activity
  static final List<ActivityItem> recentActivity = [
    ActivityItem(
      title: 'Anxiety score improved',
      description: 'Your anxiety score improved 15% this month 📈',
      timestamp: DateTime.now().subtract(const Duration(hours: 2)),
      icon: Icons.trending_up,
      color: const Color(0xFF81B29A),
    ),
    ActivityItem(
      title: 'New journal insight',
      description: 'New journal insight available from your Philosopher persona',
      timestamp: DateTime.now().subtract(const Duration(hours: 5)),
      icon: Icons.lightbulb,
      color: const Color(0xFF7BA5C6),
    ),
    ActivityItem(
      title: 'Treatment plan shared',
      description: 'Dr. Sarah Johnson shared your treatment plan',
      timestamp: DateTime.now().subtract(const Duration(days: 1)),
      icon: Icons.medical_services,
      color: const Color(0xFF5A9B9B),
    ),
    ActivityItem(
      title: 'Achievement unlocked',
      description: 'Achievement unlocked: 30-day tracking streak! 🎉',
      timestamp: DateTime.now().subtract(const Duration(days: 1)),
      icon: Icons.emoji_events,
      color: const Color(0xFFF2A65A),
    ),
  ];

  // Wearable Data
  static final List<WearableData> wearableData = [
    WearableData(name: 'Steps', value: '8,450', icon: Icons.directions_walk),
    WearableData(name: 'HRV', value: '65 ms', icon: Icons.favorite),
    WearableData(name: 'Sleep Score', value: '82/100', icon: Icons.bedtime),
  ];

  // Recommended Practitioners
  static final List<Practitioner> recommendedPractitioners = [
    Practitioner(
      name: 'Dr. Michael Chen',
      title: 'Licensed Acupuncturist',
      specialty: 'Stress & Pain Management',
      sanaIndex: 92.0,
      imageUrl: 'https://i.pravatar.cc/300?img=12',
      yearsExperience: 12,
      clientsGraduated: 650,
      totalSessions: 3200,
      rating: 4.9,
      reviewCount: 312,
    ),
    Practitioner(
      name: 'Emma Williams',
      title: 'Nutritional Therapist',
      specialty: 'Gut Health & Inflammation',
      sanaIndex: 85.0,
      imageUrl: 'https://i.pravatar.cc/300?img=5',
      yearsExperience: 6,
      clientsGraduated: 340,
      totalSessions: 1800,
      rating: 4.7,
      reviewCount: 189,
    ),
    Practitioner(
      name: 'Dr. James Martinez',
      title: 'Functional Medicine',
      specialty: 'Hormones & Metabolism',
      sanaIndex: 89.0,
      imageUrl: 'https://i.pravatar.cc/300?img=33',
      yearsExperience: 10,
      clientsGraduated: 520,
      totalSessions: 2600,
      rating: 4.8,
      reviewCount: 267,
    ),
  ];
}
