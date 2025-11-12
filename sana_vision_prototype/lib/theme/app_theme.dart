import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // SANA Brand Colors
  static const Color primaryGreen = Color(0xFF6B9080);
  static const Color secondaryBlue = Color(0xFF7BA5C6);
  static const Color accentTeal = Color(0xFF5A9B9B);
  static const Color warmNeutral = Color(0xFFEAE7DC);
  static const Color lightCream = Color(0xFFF8F6F3);
  static const Color darkGreen = Color(0xFF4A6D5B);

  // Status Colors
  static const Color statusNeedsSupport = Color(0xFFE07A5F);
  static const Color statusStable = Color(0xFFF4A261);
  static const Color statusThriving = Color(0xFF7BA5C6);
  static const Color statusOptimal = Color(0xFF6B9080);
  static const Color statusRadiant = Color(0xFF5A9B9B);

  // Functional Colors
  static const Color successGreen = Color(0xFF81B29A);
  static const Color warningOrange = Color(0xFFF2A65A);
  static const Color errorRed = Color(0xFFD56F6F);
  static const Color infoBlue = Color(0xFF7BA5C6);

  // Text Colors
  static const Color textPrimary = Color(0xFF2C3E50);
  static const Color textSecondary = Color(0xFF6C7A89);
  static const Color textLight = Color(0xFF95A5A6);

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.light(
        primary: primaryGreen,
        secondary: secondaryBlue,
        tertiary: accentTeal,
        surface: Colors.white,
        background: lightCream,
        error: errorRed,
        onPrimary: Colors.white,
        onSecondary: Colors.white,
        onSurface: textPrimary,
        onBackground: textPrimary,
      ),
      textTheme: GoogleFonts.interTextTheme(
        const TextTheme(
          displayLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: textPrimary),
          displayMedium: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: textPrimary),
          displaySmall: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: textPrimary),
          headlineLarge: TextStyle(fontSize: 22, fontWeight: FontWeight.w600, color: textPrimary),
          headlineMedium: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: textPrimary),
          headlineSmall: TextStyle(fontSize: 18, fontWeight: FontWeight.w600, color: textPrimary),
          titleLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: textPrimary),
          titleMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: textPrimary),
          titleSmall: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: textPrimary),
          bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.normal, color: textPrimary),
          bodyMedium: TextStyle(fontSize: 14, fontWeight: FontWeight.normal, color: textPrimary),
          bodySmall: TextStyle(fontSize: 12, fontWeight: FontWeight.normal, color: textSecondary),
          labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: textPrimary),
          labelMedium: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: textSecondary),
          labelSmall: TextStyle(fontSize: 10, fontWeight: FontWeight.w500, color: textLight),
        ),
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: Colors.white,
        foregroundColor: textPrimary,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.inter(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: textPrimary,
        ),
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        color: Colors.white,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryGreen,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          elevation: 2,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: warmNeutral.withOpacity(0.3),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: primaryGreen, width: 2),
        ),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: warmNeutral,
        labelStyle: const TextStyle(color: textPrimary),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      ),
    );
  }

  // Helper function to get status color
  static Color getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'needs support':
        return statusNeedsSupport;
      case 'stable':
        return statusStable;
      case 'thriving':
        return statusThriving;
      case 'optimal':
        return statusOptimal;
      case 'radiant':
        return statusRadiant;
      default:
        return primaryGreen;
    }
  }

  // Helper function to get status emoji
  static String getStatusEmoji(String status) {
    switch (status.toLowerCase()) {
      case 'needs support':
        return '🌱';
      case 'stable':
        return '🌿';
      case 'thriving':
        return '🌟';
      case 'optimal':
        return '✨';
      case 'radiant':
        return '🌈';
      default:
        return '🌿';
    }
  }
}
