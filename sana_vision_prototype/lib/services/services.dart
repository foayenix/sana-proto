/// SANA Services
/// Export all service classes
library;

export 'api_service.dart';
export 'auth_service.dart';
export 'health_service.dart';
export 'practitioner_service.dart';

// Additional services - Journal, Wearables, Scanner, etc.

import 'api_service.dart';

/// Journal Entry model
class JournalEntry {
  final String id;
  final String content;
  final String? mood;
  final List<String> tags;
  final Map<String, String>? aiResponses;
  final String? selectedPersona;
  final DateTime createdAt;

  JournalEntry({
    required this.id,
    required this.content,
    this.mood,
    this.tags = const [],
    this.aiResponses,
    this.selectedPersona,
    required this.createdAt,
  });

  factory JournalEntry.fromJson(Map<String, dynamic> json) {
    return JournalEntry(
      id: json['id'] ?? '',
      content: json['content'] ?? '',
      mood: json['mood'],
      tags: List<String>.from(json['tags'] ?? []),
      aiResponses: json['ai_responses'] != null
          ? Map<String, String>.from(json['ai_responses'])
          : null,
      selectedPersona: json['selected_persona'],
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
    );
  }
}

/// Wearable data summary
class WearableSummary {
  final DateTime date;
  final int? steps;
  final int? activeMinutes;
  final double? sleepHours;
  final int? sleepScore;
  final int? hrv;
  final int? restingHr;
  final int? stressScore;

  WearableSummary({
    required this.date,
    this.steps,
    this.activeMinutes,
    this.sleepHours,
    this.sleepScore,
    this.hrv,
    this.restingHr,
    this.stressScore,
  });

  factory WearableSummary.fromJson(Map<String, dynamic> json) {
    return WearableSummary(
      date: DateTime.tryParse(json['date'] ?? '') ?? DateTime.now(),
      steps: json['steps'] as int?,
      activeMinutes: json['active_minutes'] as int?,
      sleepHours: (json['sleep_hours'] as num?)?.toDouble(),
      sleepScore: json['sleep_score'] as int?,
      hrv: json['hrv'] as int?,
      restingHr: json['resting_hr'] as int?,
      stressScore: json['stress_score'] as int?,
    );
  }
}

/// Product from scanner
class ScannedProduct {
  final String id;
  final String? barcode;
  final String name;
  final String brand;
  final String category;
  final List<String> ingredients;
  final String dosage;
  final double safetyScore;
  final double shiAvg;
  final List<String> warnings;
  final String? imageUrl;

  ScannedProduct({
    required this.id,
    this.barcode,
    required this.name,
    required this.brand,
    required this.category,
    required this.ingredients,
    required this.dosage,
    required this.safetyScore,
    required this.shiAvg,
    required this.warnings,
    this.imageUrl,
  });

  factory ScannedProduct.fromJson(Map<String, dynamic> json) {
    return ScannedProduct(
      id: json['id'] ?? '',
      barcode: json['barcode'],
      name: json['name'] ?? '',
      brand: json['brand'] ?? '',
      category: json['category'] ?? '',
      ingredients: List<String>.from(json['ingredients'] ?? []),
      dosage: json['dosage'] ?? '',
      safetyScore: (json['safety_score'] as num?)?.toDouble() ?? 0.0,
      shiAvg: (json['shi_avg'] as num?)?.toDouble() ?? 0.0,
      warnings: List<String>.from(json['warnings'] ?? []),
      imageUrl: json['image_url'],
    );
  }
}

/// Journal Service (SIRM)
class JournalService {
  static final JournalService _instance = JournalService._internal();
  factory JournalService() => _instance;
  JournalService._internal();

  final ApiService _api = ApiService();

  /// Get AI personas
  List<Map<String, dynamic>> get personas => [
        {
          'id': 'therapist',
          'name': 'Compassionate Therapist',
          'emoji': '🧘',
          'description': 'Warm, empathetic guidance'
        },
        {
          'id': 'philosopher',
          'name': 'Wise Philosopher',
          'emoji': '📚',
          'description': 'Deep wisdom and perspective'
        },
        {
          'id': 'poet',
          'name': 'Creative Poet',
          'emoji': '🎨',
          'description': 'Artistic expression'
        },
        {
          'id': 'coach',
          'name': 'Evidence-Based Coach',
          'emoji': '🔬',
          'description': 'Practical strategies'
        },
      ];

  /// Get AI insight for journal entry
  Future<Map<String, String>?> getInsight({
    required String content,
    required String personaId,
  }) async {
    // In production: Call SIRM API
    // For demo: Return mock responses
    final responses = {
      'therapist':
          'I hear the weight in your words, and I want you to know that what you\'re feeling is valid. '
              'It takes courage to express these thoughts. Remember that each day brings new opportunities for growth.',
      'philosopher':
          'Your reflection reminds me of what Seneca wrote: "We suffer more in imagination than in reality." '
              'Perhaps consider what this moment is teaching you about your own resilience.',
      'poet':
          'In the garden of your mind,\nThoughts bloom like spring flowers—\nSome bright, some shadowed.\nTend them all with gentle hands.',
      'coach':
          'Based on what you\'ve shared, here are 3 evidence-based strategies:\n'
              '1. Practice 4-7-8 breathing for 5 minutes\n'
              '2. Write down 3 things within your control\n'
              '3. Schedule a 10-minute walk outdoors',
    };

    return {personaId: responses[personaId] ?? 'Insight not available'};
  }

  /// Create journal entry
  Future<JournalEntry?> createEntry({
    required String userId,
    required String content,
    String? mood,
    List<String>? tags,
    String? selectedPersona,
  }) async {
    final response = await _api.post(
      '/journal/entries',
      body: {
        'user_id': userId,
        'content': content,
        if (mood != null) 'mood': mood,
        if (tags != null) 'tags': tags,
        if (selectedPersona != null) 'selected_persona': selectedPersona,
      },
    );

    if (response.success && response.data != null) {
      return JournalEntry.fromJson(response.data!);
    }
    return null;
  }

  /// Get journal history
  Future<List<JournalEntry>> getHistory(String userId, {int limit = 20}) async {
    final response = await _api.get(
      '/journal/entries/$userId',
      queryParams: {'limit': limit.toString()},
    );

    if (response.success && response.data != null) {
      final entries = response.data!['entries'] as List? ?? [];
      return entries
          .map((e) => JournalEntry.fromJson(e as Map<String, dynamic>))
          .toList();
    }
    return [];
  }
}

/// Wearables Service
class WearablesService {
  static final WearablesService _instance = WearablesService._internal();
  factory WearablesService() => _instance;
  WearablesService._internal();

  final ApiService _api = ApiService();

  /// Get supported providers
  Future<List<Map<String, dynamic>>> getProviders() async {
    final response = await _api.get('${ApiConfig.wearables}/providers');
    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(response.data as List);
    }
    return [];
  }

  /// Connect wearable
  Future<bool> connectWearable(String userId, String provider) async {
    final response = await _api.post(
      '${ApiConfig.wearables}/connect',
      body: {'user_id': userId, 'provider': provider},
    );
    return response.success;
  }

  /// Get daily summaries
  Future<List<WearableSummary>> getSummaries(String userId,
      {int limit = 7}) async {
    final response = await _api.get(
      '${ApiConfig.wearables}/summaries/$userId',
      queryParams: {'limit': limit.toString()},
    );

    if (response.success && response.data != null) {
      final summaries = response.data!['summaries'] as List? ?? [];
      return summaries
          .map((s) => WearableSummary.fromJson(s as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Sync wearable data
  Future<bool> syncData(String connectionId) async {
    final response = await _api.post('${ApiConfig.wearables}/sync/$connectionId');
    return response.success;
  }
}

/// Scanner Service
class ScannerService {
  static final ScannerService _instance = ScannerService._internal();
  factory ScannerService() => _instance;
  ScannerService._internal();

  final ApiService _api = ApiService();

  /// Scan barcode
  Future<ScannedProduct?> scanBarcode(String barcode) async {
    final response = await _api.post(
      '${ApiConfig.scanner}/barcode',
      body: {'barcode': barcode},
    );

    if (response.success && response.data != null) {
      if (response.data!['found'] == true) {
        return ScannedProduct.fromJson(
            response.data!['product'] as Map<String, dynamic>);
      }
    }
    return null;
  }

  /// Check product safety
  Future<Map<String, dynamic>?> checkSafety({
    required String productId,
    List<String>? medications,
    List<String>? conditions,
  }) async {
    final response = await _api.post(
      '${ApiConfig.scanner}/safety-check',
      body: {
        'product_id': productId,
        if (medications != null) 'medications': medications,
        if (conditions != null) 'conditions': conditions,
      },
    );

    if (response.success && response.data != null) {
      return response.data;
    }
    return null;
  }

  /// Search products
  Future<List<ScannedProduct>> searchProducts(String query) async {
    final response = await _api.get(
      '${ApiConfig.scanner}/products/search',
      queryParams: {'q': query},
    );

    if (response.success && response.data != null) {
      final products = response.data!['results'] as List? ?? [];
      return products
          .map((p) => ScannedProduct.fromJson(p as Map<String, dynamic>))
          .toList();
    }
    return [];
  }
}

/// Safety Service (SST)
class SafetyService {
  static final SafetyService _instance = SafetyService._internal();
  factory SafetyService() => _instance;
  SafetyService._internal();

  final ApiService _api = ApiService();

  /// Analyze safety from text
  Future<Map<String, dynamic>?> analyzeSafety({
    required String userId,
    String? text,
    List<String>? symptoms,
  }) async {
    final response = await _api.post(
      '${ApiConfig.safety}/analyze',
      body: {
        'user_id': userId,
        if (text != null) 'text': text,
        if (symptoms != null) 'symptoms': symptoms,
      },
    );

    if (response.success && response.data != null) {
      return response.data;
    }
    return null;
  }

  /// Get safety resources
  Future<List<Map<String, dynamic>>> getResources({String? category}) async {
    final queryParams = <String, String>{};
    if (category != null) queryParams['category'] = category;

    final response = await _api.get(
      '${ApiConfig.safety}/resources',
      queryParams: queryParams.isNotEmpty ? queryParams : null,
    );

    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(response.data as List);
    }
    return [];
  }

  /// Check herb-drug interactions
  Future<Map<String, dynamic>?> checkInteractions({
    required List<String> herbs,
    List<String>? medications,
  }) async {
    final response = await _api.post(
      '${ApiConfig.safety}/check-interaction',
      body: {
        'herbs': herbs,
        if (medications != null) 'medications': medications,
      },
    );

    if (response.success && response.data != null) {
      return response.data;
    }
    return null;
  }
}
