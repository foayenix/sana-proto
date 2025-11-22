import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // SANA Brand Colors - Premium Sage Palette
  static const Color primaryGreen = Color(0xFF4A7C59);
  static const Color secondaryBlue = Color(0xFF3B82F6);
  static const Color accentTeal = Color(0xFF14B8A6);
  static const Color warmNeutral = Color(0xFFF1F5F9);
  static const Color lightCream = Color(0xFFFAFAFA);
  static const Color darkGreen = Color(0xFF365D42);

  // Premium Gradient Colors
  static const Color gradientPurpleStart = Color(0xFF8B5CF6);
  static const Color gradientPurpleEnd = Color(0xFF6366F1);
  static const Color gradientTealStart = Color(0xFF10B981);
  static const Color gradientTealEnd = Color(0xFF14B8A6);
  static const Color gradientBlueStart = Color(0xFF3B82F6);
  static const Color gradientBlueEnd = Color(0xFF06B6D4);
  static const Color gradientRoseStart = Color(0xFFEC4899);
  static const Color gradientRoseEnd = Color(0xFFF43F5E);
  static const Color gradientAmberStart = Color(0xFFF59E0B);
  static const Color gradientAmberEnd = Color(0xFFF97316);

  // Status Colors - More vibrant
  static const Color statusNeedsSupport = Color(0xFFF59E0B);
  static const Color statusStable = Color(0xFF22C55E);
  static const Color statusThriving = Color(0xFF10B981);
  static const Color statusOptimal = Color(0xFF8B5CF6);
  static const Color statusRadiant = Color(0xFFEC4899);

  // Functional Colors
  static const Color successGreen = Color(0xFF22C55E);
  static const Color warningOrange = Color(0xFFF59E0B);
  static const Color errorRed = Color(0xFFEF4444);
  static const Color infoBlue = Color(0xFF3B82F6);

  // Text Colors
  static const Color textPrimary = Color(0xFF1E293B);
  static const Color textSecondary = Color(0xFF64748B);
  static const Color textLight = Color(0xFF94A3B8);

  // Premium Gradients
  static const LinearGradient healingGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [gradientTealStart, gradientTealEnd],
  );

  static const LinearGradient techGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [gradientPurpleStart, gradientPurpleEnd],
  );

  static const LinearGradient trustGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [gradientBlueStart, gradientBlueEnd],
  );

  static const LinearGradient vitalityGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [gradientAmberStart, gradientAmberEnd],
  );

  static const LinearGradient careGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [gradientRoseStart, gradientRoseEnd],
  );

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

  // Helper function to get status icon (replacing emojis)
  static IconData getStatusIcon(String status) {
    switch (status.toLowerCase()) {
      case 'needs support':
      case 'needs attention':
        return Icons.eco_outlined;
      case 'stable':
      case 'fair':
        return Icons.spa_outlined;
      case 'thriving':
      case 'good':
        return Icons.local_florist_outlined;
      case 'optimal':
        return Icons.auto_awesome;
      case 'radiant':
        return Icons.brightness_7;
      default:
        return Icons.spa_outlined;
    }
  }

  // Helper function to get status gradient colors
  static List<Color> getStatusGradient(String status) {
    switch (status.toLowerCase()) {
      case 'needs support':
      case 'needs attention':
        return [gradientAmberStart, gradientAmberEnd];
      case 'stable':
      case 'fair':
        return [const Color(0xFF22C55E), gradientTealStart];
      case 'thriving':
      case 'good':
        return [gradientTealStart, gradientTealEnd];
      case 'optimal':
        return [gradientPurpleStart, gradientPurpleEnd];
      case 'radiant':
        return [gradientRoseStart, gradientPurpleStart];
      default:
        return [gradientTealStart, gradientTealEnd];
    }
  }

  // Premium box shadow
  static List<BoxShadow> premiumShadow(Color color) {
    return [
      BoxShadow(
        color: color.withOpacity(0.25),
        blurRadius: 12,
        offset: const Offset(0, 4),
      ),
    ];
  }

  // Card decoration with premium styling
  static BoxDecoration get premiumCardDecoration => BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(20),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withOpacity(0.04),
        blurRadius: 20,
        offset: const Offset(0, 4),
      ),
    ],
  );
}
