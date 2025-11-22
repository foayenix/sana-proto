/// SANA Authentication Service
/// Handles user registration, login, and token management
library;

import 'api_service.dart';

/// User model
class User {
  final String id;
  final String email;
  final String? firstName;
  final String? lastName;
  final String role;
  final String subscriptionTier;
  final bool isVerified;

  User({
    required this.id,
    required this.email,
    this.firstName,
    this.lastName,
    required this.role,
    required this.subscriptionTier,
    required this.isVerified,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] ?? '',
      email: json['email'] ?? '',
      firstName: json['first_name'],
      lastName: json['last_name'],
      role: json['role'] ?? 'client',
      subscriptionTier: json['subscription_tier'] ?? 'free',
      isVerified: json['is_verified'] ?? false,
    );
  }

  String get fullName => [firstName, lastName].where((n) => n != null).join(' ');
}

/// Authentication result
class AuthResult {
  final bool success;
  final User? user;
  final String? accessToken;
  final String? refreshToken;
  final String? error;

  AuthResult({
    required this.success,
    this.user,
    this.accessToken,
    this.refreshToken,
    this.error,
  });
}

/// Authentication Service
class AuthService {
  static final AuthService _instance = AuthService._internal();
  factory AuthService() => _instance;
  AuthService._internal();

  final ApiService _api = ApiService();
  User? _currentUser;

  User? get currentUser => _currentUser;
  bool get isAuthenticated => _currentUser != null;

  /// Register new user
  Future<AuthResult> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
    String role = 'client',
  }) async {
    final response = await _api.post(
      '${ApiConfig.auth}/register',
      body: {
        'email': email,
        'password': password,
        if (firstName != null) 'first_name': firstName,
        if (lastName != null) 'last_name': lastName,
        'role': role,
      },
      requiresAuth: false,
    );

    if (response.success && response.data != null) {
      final accessToken = response.data!['access_token'] as String;
      _api.setAuthToken(accessToken);

      return AuthResult(
        success: true,
        accessToken: accessToken,
        refreshToken: response.data!['refresh_token'] as String?,
        user: User.fromJson(response.data!['user'] as Map<String, dynamic>),
      );
    }

    return AuthResult(
      success: false,
      error: response.error ?? 'Registration failed',
    );
  }

  /// Login user
  Future<AuthResult> login({
    required String email,
    required String password,
  }) async {
    final response = await _api.post(
      '${ApiConfig.auth}/login',
      body: {
        'email': email,
        'password': password,
      },
      requiresAuth: false,
    );

    if (response.success && response.data != null) {
      final accessToken = response.data!['access_token'] as String;
      _api.setAuthToken(accessToken);

      final userData = response.data!['user'] as Map<String, dynamic>;
      _currentUser = User.fromJson(userData);

      return AuthResult(
        success: true,
        accessToken: accessToken,
        refreshToken: response.data!['refresh_token'] as String?,
        user: _currentUser,
      );
    }

    return AuthResult(
      success: false,
      error: response.error ?? 'Login failed',
    );
  }

  /// Get current user profile
  Future<User?> getCurrentUser() async {
    final response = await _api.get('${ApiConfig.auth}/me');

    if (response.success && response.data != null) {
      _currentUser = User.fromJson(response.data!);
      return _currentUser;
    }

    return null;
  }

  /// Logout user
  Future<void> logout() async {
    await _api.post('${ApiConfig.auth}/logout');
    _api.clearAuthToken();
    _currentUser = null;
  }

  /// Refresh access token
  Future<bool> refreshToken(String refreshToken) async {
    final response = await _api.post(
      '${ApiConfig.auth}/refresh',
      body: {'refresh_token': refreshToken},
      requiresAuth: false,
    );

    if (response.success && response.data != null) {
      final accessToken = response.data!['access_token'] as String;
      _api.setAuthToken(accessToken);
      return true;
    }

    return false;
  }
}
