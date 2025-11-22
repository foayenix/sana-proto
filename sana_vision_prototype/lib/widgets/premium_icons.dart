/// SANA Premium Icon System
/// Replaces generic emojis with sophisticated gradient icons
library;

import 'package:flutter/material.dart';

/// Premium gradient icon container
class PremiumIcon extends StatelessWidget {
  final IconData icon;
  final List<Color> gradientColors;
  final double size;
  final double iconSize;
  final double borderRadius;
  final bool hasShadow;

  const PremiumIcon({
    super.key,
    required this.icon,
    required this.gradientColors,
    this.size = 48,
    this.iconSize = 24,
    this.borderRadius = 14,
    this.hasShadow = true,
  });

  // ===== PRESET GRADIENTS =====

  /// Healing/Natural - Emerald to Teal
  static const List<Color> healingGradient = [
    Color(0xFF10B981),
    Color(0xFF14B8A6),
  ];

  /// AI/Tech - Purple to Indigo
  static const List<Color> techGradient = [
    Color(0xFF8B5CF6),
    Color(0xFF6366F1),
  ];

  /// Evidence/Trust - Blue to Cyan
  static const List<Color> trustGradient = [
    Color(0xFF3B82F6),
    Color(0xFF06B6D4),
  ];

  /// Vitality/Energy - Amber to Orange
  static const List<Color> vitalityGradient = [
    Color(0xFFF59E0B),
    Color(0xFFF97316),
  ];

  /// Calm/Balance - Indigo to Purple
  static const List<Color> calmGradient = [
    Color(0xFF6366F1),
    Color(0xFF8B5CF6),
  ];

  /// Rose/Care - Pink to Rose
  static const List<Color> careGradient = [
    Color(0xFFEC4899),
    Color(0xFFF43F5E),
  ];

  /// Success/Verified - Green
  static const List<Color> successGradient = [
    Color(0xFF22C55E),
    Color(0xFF10B981),
  ];

  /// Warning/Caution - Amber
  static const List<Color> warningGradient = [
    Color(0xFFFBBF24),
    Color(0xFFF59E0B),
  ];

  /// Sage/Brand - SANA brand colors
  static const List<Color> sageGradient = [
    Color(0xFF4A7C59),
    Color(0xFF5B8A6A),
  ];

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: gradientColors,
        ),
        borderRadius: BorderRadius.circular(borderRadius),
        boxShadow: hasShadow
            ? [
                BoxShadow(
                  color: gradientColors.first.withOpacity(0.3),
                  blurRadius: 12,
                  offset: const Offset(0, 4),
                ),
              ]
            : null,
      ),
      child: Icon(
        icon,
        color: Colors.white,
        size: iconSize,
      ),
    );
  }
}

/// Status indicator with premium styling
class PremiumStatusBadge extends StatelessWidget {
  final String status;
  final double size;

  const PremiumStatusBadge({
    super.key,
    required this.status,
    this.size = 32,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getStatusConfig(status);

    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: config.colors,
        ),
        shape: BoxShape.circle,
        boxShadow: [
          BoxShadow(
            color: config.colors.first.withOpacity(0.3),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Icon(
        config.icon,
        color: Colors.white,
        size: size * 0.5,
      ),
    );
  }

  _StatusConfig _getStatusConfig(String status) {
    switch (status.toLowerCase()) {
      case 'needs support':
      case 'needs attention':
        return _StatusConfig(
          colors: [const Color(0xFFFBBF24), const Color(0xFFF59E0B)],
          icon: Icons.eco_outlined,
        );
      case 'stable':
      case 'fair':
        return _StatusConfig(
          colors: [const Color(0xFF22C55E), const Color(0xFF10B981)],
          icon: Icons.spa_outlined,
        );
      case 'thriving':
      case 'good':
        return _StatusConfig(
          colors: [const Color(0xFF10B981), const Color(0xFF14B8A6)],
          icon: Icons.local_florist_outlined,
        );
      case 'optimal':
        return _StatusConfig(
          colors: [const Color(0xFF8B5CF6), const Color(0xFF6366F1)],
          icon: Icons.auto_awesome,
        );
      case 'radiant':
        return _StatusConfig(
          colors: [const Color(0xFFEC4899), const Color(0xFF8B5CF6)],
          icon: Icons.brightness_7,
        );
      default:
        return _StatusConfig(
          colors: [const Color(0xFF6B7280), const Color(0xFF4B5563)],
          icon: Icons.circle_outlined,
        );
    }
  }
}

class _StatusConfig {
  final List<Color> colors;
  final IconData icon;

  _StatusConfig({required this.colors, required this.icon});
}

/// Mood indicator with premium styling
class PremiumMoodIcon extends StatelessWidget {
  final String mood;
  final double size;

  const PremiumMoodIcon({
    super.key,
    required this.mood,
    this.size = 40,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getMoodConfig(mood);

    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: config.colors,
        ),
        borderRadius: BorderRadius.circular(size * 0.3),
        boxShadow: [
          BoxShadow(
            color: config.colors.first.withOpacity(0.25),
            blurRadius: 10,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Icon(
        config.icon,
        color: Colors.white,
        size: size * 0.5,
      ),
    );
  }

  _MoodConfig _getMoodConfig(String mood) {
    switch (mood.toLowerCase()) {
      case 'happy':
      case 'good':
      case 'great':
        return _MoodConfig(
          colors: [const Color(0xFF22C55E), const Color(0xFF10B981)],
          icon: Icons.sentiment_very_satisfied_rounded,
        );
      case 'calm':
      case 'peaceful':
      case 'relaxed':
        return _MoodConfig(
          colors: [const Color(0xFF6366F1), const Color(0xFF8B5CF6)],
          icon: Icons.sentiment_satisfied_rounded,
        );
      case 'tired':
      case 'sleepy':
        return _MoodConfig(
          colors: [const Color(0xFF3B82F6), const Color(0xFF6366F1)],
          icon: Icons.bedtime_rounded,
        );
      case 'anxious':
      case 'stressed':
      case 'worried':
        return _MoodConfig(
          colors: [const Color(0xFFF59E0B), const Color(0xFFF97316)],
          icon: Icons.sentiment_dissatisfied_rounded,
        );
      case 'sad':
      case 'down':
        return _MoodConfig(
          colors: [const Color(0xFF64748B), const Color(0xFF475569)],
          icon: Icons.sentiment_very_dissatisfied_rounded,
        );
      case 'energetic':
      case 'motivated':
        return _MoodConfig(
          colors: [const Color(0xFFF97316), const Color(0xFFEF4444)],
          icon: Icons.bolt_rounded,
        );
      default:
        return _MoodConfig(
          colors: [const Color(0xFF10B981), const Color(0xFF14B8A6)],
          icon: Icons.sentiment_neutral_rounded,
        );
    }
  }
}

class _MoodConfig {
  final List<Color> colors;
  final IconData icon;

  _MoodConfig({required this.colors, required this.icon});
}

/// AI Persona badge with premium styling
class PremiumPersonaBadge extends StatelessWidget {
  final String personaId;
  final double size;
  final bool showLabel;

  const PremiumPersonaBadge({
    super.key,
    required this.personaId,
    this.size = 56,
    this.showLabel = false,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getPersonaConfig(personaId);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: config.colors,
            ),
            borderRadius: BorderRadius.circular(size * 0.28),
            boxShadow: [
              BoxShadow(
                color: config.colors.first.withOpacity(0.35),
                blurRadius: 14,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Icon(
            config.icon,
            color: Colors.white,
            size: size * 0.5,
          ),
        ),
        if (showLabel) ...[
          const SizedBox(height: 8),
          Text(
            config.label,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: config.colors.first,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ],
    );
  }

  _PersonaConfig _getPersonaConfig(String personaId) {
    switch (personaId.toLowerCase()) {
      case 'therapist':
      case 'compassionate therapist':
        return _PersonaConfig(
          colors: [const Color(0xFF8B5CF6), const Color(0xFFA78BFA)],
          icon: Icons.self_improvement_rounded,
          label: 'Therapist',
        );
      case 'philosopher':
      case 'wise philosopher':
        return _PersonaConfig(
          colors: [const Color(0xFF3B82F6), const Color(0xFF60A5FA)],
          icon: Icons.menu_book_rounded,
          label: 'Philosopher',
        );
      case 'poet':
      case 'creative poet':
        return _PersonaConfig(
          colors: [const Color(0xFFEC4899), const Color(0xFFF472B6)],
          icon: Icons.brush_rounded,
          label: 'Poet',
        );
      case 'coach':
      case 'evidence-based coach':
        return _PersonaConfig(
          colors: [const Color(0xFF10B981), const Color(0xFF34D399)],
          icon: Icons.science_rounded,
          label: 'Coach',
        );
      default:
        return _PersonaConfig(
          colors: [const Color(0xFF6B7280), const Color(0xFF9CA3AF)],
          icon: Icons.psychology_rounded,
          label: 'AI',
        );
    }
  }
}

class _PersonaConfig {
  final List<Color> colors;
  final IconData icon;
  final String label;

  _PersonaConfig({
    required this.colors,
    required this.icon,
    required this.label,
  });
}

/// Star rating with premium styling
class PremiumStarRating extends StatelessWidget {
  final double rating;
  final double size;
  final Color activeColor;
  final Color inactiveColor;

  const PremiumStarRating({
    super.key,
    required this.rating,
    this.size = 18,
    this.activeColor = const Color(0xFFF59E0B),
    this.inactiveColor = const Color(0xFFE5E7EB),
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(5, (index) {
        final fill = (rating - index).clamp(0.0, 1.0);
        return Padding(
          padding: const EdgeInsets.only(right: 2),
          child: ShaderMask(
            blendMode: BlendMode.srcIn,
            shaderCallback: (bounds) {
              return LinearGradient(
                colors: fill > 0
                    ? [const Color(0xFFF59E0B), const Color(0xFFFBBF24)]
                    : [inactiveColor, inactiveColor],
              ).createShader(bounds);
            },
            child: Icon(
              fill >= 1
                  ? Icons.star_rounded
                  : (fill > 0 ? Icons.star_half_rounded : Icons.star_outline_rounded),
              size: size,
            ),
          ),
        );
      }),
    );
  }
}

/// Integration/Platform icon with brand styling
class PremiumIntegrationIcon extends StatelessWidget {
  final String platform;
  final double size;

  const PremiumIntegrationIcon({
    super.key,
    required this.platform,
    this.size = 44,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getPlatformConfig(platform);

    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: config.colors,
        ),
        borderRadius: BorderRadius.circular(size * 0.25),
        boxShadow: [
          BoxShadow(
            color: config.colors.first.withOpacity(0.25),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Icon(
        config.icon,
        color: Colors.white,
        size: size * 0.5,
      ),
    );
  }

  _PlatformConfig _getPlatformConfig(String platform) {
    switch (platform.toLowerCase()) {
      case 'apple health':
      case 'apple':
        return _PlatformConfig(
          colors: [const Color(0xFFFF2D55), const Color(0xFFFF375F)],
          icon: Icons.favorite_rounded,
        );
      case 'oura':
      case 'oura ring':
        return _PlatformConfig(
          colors: [const Color(0xFF1A1A2E), const Color(0xFF16213E)],
          icon: Icons.circle_outlined,
        );
      case 'fitbit':
        return _PlatformConfig(
          colors: [const Color(0xFF00B0B9), const Color(0xFF00CED1)],
          icon: Icons.watch_rounded,
        );
      case 'whoop':
        return _PlatformConfig(
          colors: [const Color(0xFF000000), const Color(0xFF2D2D2D)],
          icon: Icons.fitness_center_rounded,
        );
      case 'garmin':
        return _PlatformConfig(
          colors: [const Color(0xFF007CC3), const Color(0xFF0090D4)],
          icon: Icons.directions_run_rounded,
        );
      default:
        return _PlatformConfig(
          colors: [const Color(0xFF6B7280), const Color(0xFF9CA3AF)],
          icon: Icons.devices_rounded,
        );
    }
  }
}

class _PlatformConfig {
  final List<Color> colors;
  final IconData icon;

  _PlatformConfig({required this.colors, required this.icon});
}

/// Glassmorphic card for premium feel
class GlassmorphicCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets? padding;
  final double borderRadius;

  const GlassmorphicCard({
    super.key,
    required this.child,
    this.padding,
    this.borderRadius = 20,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: padding ?? const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.85),
        borderRadius: BorderRadius.circular(borderRadius),
        border: Border.all(
          color: Colors.white.withOpacity(0.5),
          width: 1,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: child,
    );
  }
}

/// SANA Index score display with premium gradient
class PremiumSanaIndex extends StatelessWidget {
  final double score;
  final double size;
  final bool showLabel;

  const PremiumSanaIndex({
    super.key,
    required this.score,
    this.size = 80,
    this.showLabel = true,
  });

  @override
  Widget build(BuildContext context) {
    final colors = _getScoreColors(score);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: colors,
            ),
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: colors.first.withOpacity(0.4),
                blurRadius: 20,
                offset: const Offset(0, 6),
              ),
            ],
          ),
          child: Center(
            child: Text(
              score.round().toString(),
              style: TextStyle(
                color: Colors.white,
                fontSize: size * 0.35,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        if (showLabel) ...[
          const SizedBox(height: 8),
          Text(
            'SANA Index',
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: colors.first,
              letterSpacing: 0.5,
            ),
          ),
        ],
      ],
    );
  }

  List<Color> _getScoreColors(double score) {
    if (score >= 85) {
      return [const Color(0xFF10B981), const Color(0xFF14B8A6)]; // Excellent
    } else if (score >= 70) {
      return [const Color(0xFF3B82F6), const Color(0xFF6366F1)]; // Good
    } else if (score >= 50) {
      return [const Color(0xFFF59E0B), const Color(0xFFF97316)]; // Fair
    } else {
      return [const Color(0xFFEF4444), const Color(0xFFF97316)]; // Needs work
    }
  }
}
