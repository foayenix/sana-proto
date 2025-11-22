import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ScoreCard extends StatelessWidget {
  final String title;
  final double score;
  final double? change;
  final String? subtitle;
  final Color? color;

  const ScoreCard({
    super.key,
    required this.title,
    required this.score,
    this.change,
    this.subtitle,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Text(
          title,
          style: Theme.of(context).textTheme.bodySmall,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 12),
        Stack(
          alignment: Alignment.center,
          children: [
            SizedBox(
              width: 100,
              height: 100,
              child: CircularProgressIndicator(
                value: score / 100,
                strokeWidth: 8,
                backgroundColor: AppTheme.warmNeutral,
                valueColor: AlwaysStoppedAnimation<Color>(
                  color ?? AppTheme.primaryGreen,
                ),
              ),
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  score.toStringAsFixed(0),
                  style: Theme.of(context).textTheme.displaySmall?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: color ?? AppTheme.primaryGreen,
                      ),
                ),
                Text(
                  '/100',
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ],
        ),
        if (subtitle != null) ...[
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: (color ?? AppTheme.primaryGreen).withOpacity(0.1),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  AppTheme.getStatusIcon(subtitle!),
                  size: 16,
                  color: color ?? AppTheme.primaryGreen,
                ),
                const SizedBox(width: 6),
                Text(
                  subtitle!,
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: color ?? AppTheme.primaryGreen,
                        fontWeight: FontWeight.w600,
                      ),
                ),
              ],
            ),
          ),
        ],
        if (change != null) ...[
          const SizedBox(height: 8),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                change! > 0 ? Icons.arrow_upward : Icons.arrow_downward,
                size: 14,
                color: change! > 0 ? AppTheme.successGreen : AppTheme.errorRed,
              ),
              const SizedBox(width: 4),
              Text(
                '${change!.abs().toStringAsFixed(0)} from yesterday',
                style: Theme.of(context).textTheme.labelSmall?.copyWith(
                      color: change! > 0 ? AppTheme.successGreen : AppTheme.errorRed,
                    ),
              ),
            ],
          ),
        ],
      ],
    );
  }
}
