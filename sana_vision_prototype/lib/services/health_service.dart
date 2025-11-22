/// SANA Health Service
/// Health scoring, evidence, and planning APIs
library;

import 'api_service.dart';

/// Health Score model
class HealthScore {
  final double overall;
  final String status;
  final double physical;
  final double mental;
  final double emotional;
  final double social;
  final double sleep;
  final double energy;
  final int? biologicalAge;
  final int? chronologicalAge;
  final List<Lever> topLevers;

  HealthScore({
    required this.overall,
    required this.status,
    required this.physical,
    required this.mental,
    required this.emotional,
    required this.social,
    required this.sleep,
    required this.energy,
    this.biologicalAge,
    this.chronologicalAge,
    this.topLevers = const [],
  });

  factory HealthScore.fromJson(Map<String, dynamic> json) {
    final domains = json['domains'] as List? ?? [];
    double getDomainScore(String name) {
      final domain = domains.firstWhere(
        (d) => d['domain'] == name,
        orElse: () => {'score': 0.0},
      );
      return (domain['score'] as num?)?.toDouble() ?? 0.0;
    }

    return HealthScore(
      overall: (json['overall_score'] as num?)?.toDouble() ?? 0.0,
      status: json['status'] ?? 'Unknown',
      physical: getDomainScore('Physical Health'),
      mental: getDomainScore('Mental Wellbeing'),
      emotional: getDomainScore('Emotional Balance'),
      social: getDomainScore('Social Connection'),
      sleep: getDomainScore('Sleep Quality'),
      energy: getDomainScore('Energy Levels'),
      biologicalAge: json['biological_age'] as int?,
      chronologicalAge: json['chronological_age'] as int?,
      topLevers: (json['top_levers'] as List?)
              ?.map((l) => Lever.fromJson(l as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }
}

/// Improvement lever recommendation
class Lever {
  final String domain;
  final double currentScore;
  final String recommendation;
  final String impact;

  Lever({
    required this.domain,
    required this.currentScore,
    required this.recommendation,
    required this.impact,
  });

  factory Lever.fromJson(Map<String, dynamic> json) {
    return Lever(
      domain: json['domain'] ?? '',
      currentScore: (json['current_score'] as num?)?.toDouble() ?? 0.0,
      recommendation: json['recommendation'] ?? '',
      impact: json['impact'] ?? 'medium',
    );
  }
}

/// Intervention from evidence engine
class Intervention {
  final String id;
  final String name;
  final String modality;
  final List<String> conditions;
  final String evidenceLevel;
  final double effectSize;
  final int studyCount;
  final String safetyRating;
  final String description;

  Intervention({
    required this.id,
    required this.name,
    required this.modality,
    required this.conditions,
    required this.evidenceLevel,
    required this.effectSize,
    required this.studyCount,
    required this.safetyRating,
    required this.description,
  });

  factory Intervention.fromJson(Map<String, dynamic> json) {
    return Intervention(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      modality: json['modality'] ?? '',
      conditions: List<String>.from(json['conditions'] ?? []),
      evidenceLevel: json['evidence_level'] ?? '',
      effectSize: (json['effect_size'] as num?)?.toDouble() ?? 0.0,
      studyCount: json['study_count'] ?? 0,
      safetyRating: json['safety_rating'] ?? '',
      description: json['description'] ?? '',
    );
  }
}

/// Activity from planning service
class Activity {
  final String id;
  final String name;
  final String category;
  final int durationMinutes;
  final String frequency;
  final String difficulty;
  final String evidenceLevel;
  final String description;
  final List<String>? instructions;

  Activity({
    required this.id,
    required this.name,
    required this.category,
    required this.durationMinutes,
    required this.frequency,
    required this.difficulty,
    required this.evidenceLevel,
    required this.description,
    this.instructions,
  });

  factory Activity.fromJson(Map<String, dynamic> json) {
    return Activity(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      category: json['category'] ?? '',
      durationMinutes: json['duration_minutes'] ?? 0,
      frequency: json['frequency'] ?? '',
      difficulty: json['difficulty'] ?? '',
      evidenceLevel: json['evidence_level'] ?? '',
      description: json['description'] ?? '',
      instructions: json['instructions'] != null
          ? List<String>.from(json['instructions'])
          : null,
    );
  }
}

/// Health Service for SISM, Evidence, and Planning
class HealthService {
  static final HealthService _instance = HealthService._internal();
  factory HealthService() => _instance;
  HealthService._internal();

  final ApiService _api = ApiService();

  // ========== SCORING (SISM) ==========

  /// Calculate health score
  Future<HealthScore?> calculateHealthScore(String userId) async {
    final response = await _api.post(
      '${ApiConfig.scoring}/calculate',
      body: {'user_id': userId},
    );

    if (response.success && response.data != null) {
      return HealthScore.fromJson(response.data!);
    }
    return null;
  }

  /// Get health domains
  Future<List<Map<String, dynamic>>> getDomains() async {
    final response = await _api.get('${ApiConfig.scoring}/domains');
    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(response.data!['domains'] ?? []);
    }
    return [];
  }

  /// Get health questionnaire
  Future<List<Map<String, dynamic>>> getQuestionnaire() async {
    final response = await _api.get('${ApiConfig.scoring}/questionnaire');
    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(response.data as List);
    }
    return [];
  }

  // ========== EVIDENCE (Health Graph) ==========

  /// Get interventions for a condition
  Future<List<Intervention>> getInterventions(String domain) async {
    final response = await _api.get('${ApiConfig.evidence}/interventions/$domain');

    if (response.success && response.data != null) {
      final interventions = response.data!['interventions'] as List? ?? [];
      return interventions
          .map((i) => Intervention.fromJson(i as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Search interventions
  Future<List<Intervention>> searchInterventions(String query) async {
    final response = await _api.get(
      '${ApiConfig.evidence}/search',
      queryParams: {'q': query},
    );

    if (response.success && response.data != null) {
      final interventions = response.data!['interventions'] as List? ?? [];
      return interventions
          .map((i) => Intervention.fromJson(i as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Get conditions list
  Future<List<Map<String, dynamic>>> getConditions() async {
    final response = await _api.get('${ApiConfig.evidence}/conditions');
    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(
          response.data!['conditions'] ?? []);
    }
    return [];
  }

  // ========== PLANNING (SHAM) ==========

  /// Create wellness plan
  Future<Map<String, dynamic>?> createPlan({
    required String userId,
    required List<String> goals,
    Map<String, dynamic>? preferences,
  }) async {
    final response = await _api.post(
      '${ApiConfig.planning}/create',
      body: {
        'user_id': userId,
        'goals': goals,
        if (preferences != null) 'preferences': preferences,
      },
    );

    if (response.success && response.data != null) {
      return response.data;
    }
    return null;
  }

  /// Get activities list
  Future<List<Activity>> getActivities({
    String? category,
    String? difficulty,
    int? maxDuration,
  }) async {
    final queryParams = <String, String>{};
    if (category != null) queryParams['category'] = category;
    if (difficulty != null) queryParams['difficulty'] = difficulty;
    if (maxDuration != null) queryParams['max_duration'] = maxDuration.toString();

    final response = await _api.get(
      '${ApiConfig.planning}/activities',
      queryParams: queryParams.isNotEmpty ? queryParams : null,
    );

    if (response.success && response.data != null) {
      final activities = response.data as List;
      return activities
          .map((a) => Activity.fromJson(a as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Get today's plan
  Future<Map<String, dynamic>?> getTodayPlan(String userId) async {
    final response = await _api.get('${ApiConfig.planning}/today/$userId');
    if (response.success && response.data != null) {
      return response.data;
    }
    return null;
  }

  /// Track activity completion
  Future<bool> trackActivity({
    required String userId,
    required String activityId,
    int? moodRating,
    String? notes,
  }) async {
    final response = await _api.post(
      '${ApiConfig.planning}/track',
      body: {
        'user_id': userId,
        'activity_id': activityId,
        'completed_at': DateTime.now().toIso8601String(),
        if (moodRating != null) 'mood_rating': moodRating,
        if (notes != null) 'notes': notes,
      },
    );

    return response.success;
  }
}
