import 'package:flutter/material.dart';
import '../models/dummy_data.dart';
import '../theme/app_theme.dart';

class WearableWidget extends StatelessWidget {
  final WearableData data;

  const WearableWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 100,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          Icon(
            data.icon,
            color: AppTheme.primaryGreen,
            size: 28,
          ),
          const SizedBox(height: 8),
          Text(
            data.name,
            style: Theme.of(context).textTheme.labelSmall,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 4),
          Text(
            data.value,
            style: Theme.of(context).textTheme.titleSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
