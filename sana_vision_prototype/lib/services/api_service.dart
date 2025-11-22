/// SANA API Service
/// Central HTTP client for all backend API calls
library;

import 'dart:convert';
import 'package:http/http.dart' as http;

/// Configuration for API endpoints
class ApiConfig {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const Duration timeout = Duration(seconds: 30);

  // Algorithm endpoints
  static const String scoring = '/scoring';
  static const String evidence = '/evidence';
  static const String planning = '/planning';
  static const String verification = '/verification';
  static const String matching = '/matching';
  static const String safety = '/safety';
  static const String learning = '/learning';
  static const String herbs = '/herbs';
  static const String index = '/index';

  // Service endpoints
  static const String auth = '/auth';
  static const String practice = '/practice';
  static const String marketplace = '/marketplace';
  static const String payments = '/payments';
  static const String messaging = '/messaging';
  static const String analytics = '/analytics';
  static const String wearables = '/wearables';
  static const String enterprise = '/enterprise';
  static const String widget = '/widget';
  static const String outcomes = '/outcomes';
  static const String scanner = '/scanner';
  static const String ai = '/ai';
  static const String products = '/marketplace-products';
  static const String freemium = '/freemium';
}

/// API Response wrapper
class ApiResponse<T> {
  final bool success;
  final T? data;
  final String? error;
  final int statusCode;

  ApiResponse({
    required this.success,
    this.data,
    this.error,
    required this.statusCode,
  });
}

/// Main API Service class
class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  String? _authToken;
  final http.Client _client = http.Client();

  /// Set authentication token
  void setAuthToken(String token) {
    _authToken = token;
  }

  /// Clear authentication token
  void clearAuthToken() {
    _authToken = null;
  }

  /// Build headers with optional auth
  Map<String, String> _headers({bool requiresAuth = true}) {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (requiresAuth && _authToken != null) {
      headers['Authorization'] = 'Bearer $_authToken';
    }
    return headers;
  }

  /// GET request
  Future<ApiResponse<Map<String, dynamic>>> get(
    String endpoint, {
    Map<String, String>? queryParams,
    bool requiresAuth = true,
  }) async {
    try {
      var uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      if (queryParams != null) {
        uri = uri.replace(queryParameters: queryParams);
      }

      final response = await _client
          .get(uri, headers: _headers(requiresAuth: requiresAuth))
          .timeout(ApiConfig.timeout);

      return _handleResponse(response);
    } catch (e) {
      return ApiResponse(
        success: false,
        error: e.toString(),
        statusCode: 0,
      );
    }
  }

  /// POST request
  Future<ApiResponse<Map<String, dynamic>>> post(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      final response = await _client
          .post(
            uri,
            headers: _headers(requiresAuth: requiresAuth),
            body: body != null ? jsonEncode(body) : null,
          )
          .timeout(ApiConfig.timeout);

      return _handleResponse(response);
    } catch (e) {
      return ApiResponse(
        success: false,
        error: e.toString(),
        statusCode: 0,
      );
    }
  }

  /// PUT request
  Future<ApiResponse<Map<String, dynamic>>> put(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      final response = await _client
          .put(
            uri,
            headers: _headers(requiresAuth: requiresAuth),
            body: body != null ? jsonEncode(body) : null,
          )
          .timeout(ApiConfig.timeout);

      return _handleResponse(response);
    } catch (e) {
      return ApiResponse(
        success: false,
        error: e.toString(),
        statusCode: 0,
      );
    }
  }

  /// DELETE request
  Future<ApiResponse<Map<String, dynamic>>> delete(
    String endpoint, {
    bool requiresAuth = true,
  }) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      final response = await _client
          .delete(uri, headers: _headers(requiresAuth: requiresAuth))
          .timeout(ApiConfig.timeout);

      return _handleResponse(response);
    } catch (e) {
      return ApiResponse(
        success: false,
        error: e.toString(),
        statusCode: 0,
      );
    }
  }

  /// Handle HTTP response
  ApiResponse<Map<String, dynamic>> _handleResponse(http.Response response) {
    final statusCode = response.statusCode;
    final isSuccess = statusCode >= 200 && statusCode < 300;

    Map<String, dynamic>? data;
    String? error;

    try {
      if (response.body.isNotEmpty) {
        data = jsonDecode(response.body) as Map<String, dynamic>;
      }
    } catch (e) {
      error = 'Failed to parse response';
    }

    if (!isSuccess) {
      error = data?['detail'] ?? data?['message'] ?? 'Request failed';
    }

    return ApiResponse(
      success: isSuccess,
      data: data,
      error: error,
      statusCode: statusCode,
    );
  }
}
