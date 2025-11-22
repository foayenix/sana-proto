/// SANA Practitioner Service
/// Matching, marketplace, and practice management APIs
library;

import 'api_service.dart';

/// Practitioner model
class Practitioner {
  final String id;
  final String name;
  final String title;
  final String? bio;
  final List<String> specialties;
  final List<String> modalities;
  final double sanaIndex;
  final double rating;
  final int reviewCount;
  final double hourlyRate;
  final String currency;
  final String location;
  final bool offersVideo;
  final bool offersInPerson;
  final int yearsExperience;
  final int totalClients;
  final String? imageUrl;

  Practitioner({
    required this.id,
    required this.name,
    required this.title,
    this.bio,
    required this.specialties,
    required this.modalities,
    required this.sanaIndex,
    required this.rating,
    required this.reviewCount,
    required this.hourlyRate,
    required this.currency,
    required this.location,
    required this.offersVideo,
    required this.offersInPerson,
    required this.yearsExperience,
    required this.totalClients,
    this.imageUrl,
  });

  factory Practitioner.fromJson(Map<String, dynamic> json) {
    return Practitioner(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      title: json['title'] ?? '',
      bio: json['bio'],
      specialties: List<String>.from(json['specialties'] ?? []),
      modalities: List<String>.from(json['modalities'] ?? []),
      sanaIndex: (json['sana_index'] as num?)?.toDouble() ?? 0.0,
      rating: (json['rating'] as num?)?.toDouble() ?? 0.0,
      reviewCount: json['review_count'] ?? 0,
      hourlyRate: (json['hourly_rate'] as num?)?.toDouble() ?? 0.0,
      currency: json['currency'] ?? 'GBP',
      location: json['location'] ?? '',
      offersVideo: json['offers_video'] ?? true,
      offersInPerson: json['offers_in_person'] ?? false,
      yearsExperience: json['years_experience'] ?? 0,
      totalClients: json['total_clients'] ?? 0,
      imageUrl: json['image_url'],
    );
  }
}

/// SANA Index breakdown
class SanaIndexBreakdown {
  final double credentialsScore;
  final double volumeScore;
  final double outcomesScore;
  final double completenessScore;
  final double satisfactionScore;

  SanaIndexBreakdown({
    required this.credentialsScore,
    required this.volumeScore,
    required this.outcomesScore,
    required this.completenessScore,
    required this.satisfactionScore,
  });

  factory SanaIndexBreakdown.fromJson(Map<String, dynamic> json) {
    return SanaIndexBreakdown(
      credentialsScore: (json['credentials_score'] as num?)?.toDouble() ?? 0.0,
      volumeScore: (json['volume_score'] as num?)?.toDouble() ?? 0.0,
      outcomesScore: (json['outcomes_score'] as num?)?.toDouble() ?? 0.0,
      completenessScore: (json['completeness_score'] as num?)?.toDouble() ?? 0.0,
      satisfactionScore: (json['satisfaction_score'] as num?)?.toDouble() ?? 0.0,
    );
  }

  double get total =>
      credentialsScore +
      volumeScore +
      outcomesScore +
      completenessScore +
      satisfactionScore;
}

/// Review model
class Review {
  final String id;
  final String clientName;
  final double rating;
  final String? title;
  final String content;
  final String? condition;
  final bool verified;
  final DateTime createdAt;

  Review({
    required this.id,
    required this.clientName,
    required this.rating,
    this.title,
    required this.content,
    this.condition,
    required this.verified,
    required this.createdAt,
  });

  factory Review.fromJson(Map<String, dynamic> json) {
    return Review(
      id: json['id'] ?? '',
      clientName: json['client_name'] ?? '',
      rating: (json['rating'] as num?)?.toDouble() ?? 0.0,
      title: json['title'],
      content: json['content'] ?? '',
      condition: json['condition'],
      verified: json['verified'] ?? false,
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
    );
  }
}

/// Booking model
class Booking {
  final String id;
  final String clientId;
  final String practitionerId;
  final DateTime scheduledAt;
  final int durationMinutes;
  final String sessionType;
  final double price;
  final String currency;
  final String status;
  final String? videoLink;

  Booking({
    required this.id,
    required this.clientId,
    required this.practitionerId,
    required this.scheduledAt,
    required this.durationMinutes,
    required this.sessionType,
    required this.price,
    required this.currency,
    required this.status,
    this.videoLink,
  });

  factory Booking.fromJson(Map<String, dynamic> json) {
    return Booking(
      id: json['id'] ?? '',
      clientId: json['client_id'] ?? '',
      practitionerId: json['practitioner_id'] ?? '',
      scheduledAt:
          DateTime.tryParse(json['scheduled_at'] ?? '') ?? DateTime.now(),
      durationMinutes: json['duration_minutes'] ?? 60,
      sessionType: json['session_type'] ?? 'follow_up',
      price: (json['price'] as num?)?.toDouble() ?? 0.0,
      currency: json['currency'] ?? 'GBP',
      status: json['status'] ?? 'pending',
      videoLink: json['video_link'],
    );
  }
}

/// Practitioner Service for matching and marketplace
class PractitionerService {
  static final PractitionerService _instance = PractitionerService._internal();
  factory PractitionerService() => _instance;
  PractitionerService._internal();

  final ApiService _api = ApiService();

  // ========== MATCHING (SPRM) ==========

  /// Find matching practitioners
  Future<List<Practitioner>> findPractitioners({
    required String userId,
    required List<String> conditions,
    List<String>? modalities,
    Map<String, dynamic>? preferences,
  }) async {
    final response = await _api.post(
      '${ApiConfig.matching}/find',
      body: {
        'user_id': userId,
        'conditions': conditions,
        if (modalities != null) 'modalities': modalities,
        if (preferences != null) 'preferences': preferences,
      },
    );

    if (response.success && response.data != null) {
      final matches = response.data!['matches'] as List? ?? [];
      return matches
          .map((p) => Practitioner.fromJson(p as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Quick match for single condition
  Future<List<Practitioner>> quickMatch(String condition,
      {String? location}) async {
    final queryParams = {'condition': condition};
    if (location != null) queryParams['location'] = location;

    final response = await _api.get(
      '${ApiConfig.matching}/quick-match',
      queryParams: queryParams,
    );

    if (response.success && response.data != null) {
      final matches = response.data!['matches'] as List? ?? [];
      return matches
          .map((p) => Practitioner.fromJson(p as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Get available modalities
  Future<List<Map<String, dynamic>>> getModalities() async {
    final response = await _api.get('${ApiConfig.matching}/modalities');
    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(response.data as List);
    }
    return [];
  }

  // ========== MARKETPLACE ==========

  /// Search practitioners
  Future<List<Practitioner>> searchPractitioners({
    List<String>? conditions,
    List<String>? modalities,
    String? location,
    double? maxPrice,
    double? minRating,
    String sortBy = 'relevance',
  }) async {
    final response = await _api.post(
      '${ApiConfig.marketplace}/search',
      body: {
        if (conditions != null) 'conditions': conditions,
        if (modalities != null) 'modalities': modalities,
        if (location != null) 'location': location,
        if (maxPrice != null) 'max_price': maxPrice,
        if (minRating != null) 'min_rating': minRating,
      },
    );

    if (response.success && response.data != null) {
      final practitioners = response.data!['practitioners'] as List? ?? [];
      return practitioners
          .map((p) => Practitioner.fromJson(p as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Get practitioner profile
  Future<Practitioner?> getPractitionerProfile(String practitionerId) async {
    final response = await _api.get(
      '${ApiConfig.marketplace}/practitioners/$practitionerId',
    );

    if (response.success && response.data != null) {
      return Practitioner.fromJson(response.data!);
    }
    return null;
  }

  /// Get practitioner reviews
  Future<List<Review>> getPractitionerReviews(String practitionerId) async {
    final response = await _api.get(
      '${ApiConfig.marketplace}/practitioners/$practitionerId/reviews',
    );

    if (response.success && response.data != null) {
      final reviews = response.data!['reviews'] as List? ?? [];
      return reviews
          .map((r) => Review.fromJson(r as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  /// Submit review
  Future<bool> submitReview({
    required String practitionerId,
    required double rating,
    required String content,
    String? title,
    String? condition,
  }) async {
    final response = await _api.post(
      '${ApiConfig.marketplace}/reviews',
      body: {
        'practitioner_id': practitionerId,
        'rating': rating,
        'content': content,
        if (title != null) 'title': title,
        if (condition != null) 'condition': condition,
      },
    );

    return response.success;
  }

  /// Get discovery page
  Future<Map<String, dynamic>?> getDiscoveryPage() async {
    final response = await _api.get('${ApiConfig.marketplace}/discover');
    if (response.success && response.data != null) {
      return response.data;
    }
    return null;
  }

  // ========== SANA INDEX ==========

  /// Calculate SANA Index
  Future<Map<String, dynamic>?> calculateSanaIndex(
      String practitionerId) async {
    final response = await _api.post(
      '${ApiConfig.index}/calculate',
      body: {'practitioner_id': practitionerId},
    );

    if (response.success && response.data != null) {
      return response.data;
    }
    return null;
  }

  /// Get leaderboard
  Future<List<Map<String, dynamic>>> getLeaderboard({
    String? specialty,
    int limit = 20,
  }) async {
    final queryParams = <String, String>{};
    if (specialty != null) queryParams['specialty'] = specialty;
    queryParams['limit'] = limit.toString();

    final response = await _api.get(
      '${ApiConfig.index}/leaderboard',
      queryParams: queryParams,
    );

    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(response.data as List);
    }
    return [];
  }

  // ========== PRACTICE ==========

  /// Create booking
  Future<Booking?> createBooking({
    required String clientId,
    required String practitionerId,
    required DateTime scheduledAt,
    int durationMinutes = 60,
    String sessionType = 'initial',
  }) async {
    final response = await _api.post(
      '${ApiConfig.practice}/bookings',
      body: {
        'client_id': clientId,
        'practitioner_id': practitionerId,
        'scheduled_at': scheduledAt.toIso8601String(),
        'duration_minutes': durationMinutes,
        'session_type': sessionType,
      },
    );

    if (response.success && response.data != null) {
      return Booking.fromJson(response.data!);
    }
    return null;
  }

  /// Get calendar availability
  Future<List<Map<String, dynamic>>> getCalendar(String practitionerId) async {
    final response = await _api.get(
      '${ApiConfig.practice}/calendar/$practitionerId',
    );

    if (response.success && response.data != null) {
      return List<Map<String, dynamic>>.from(response.data!['slots'] ?? []);
    }
    return [];
  }
}
