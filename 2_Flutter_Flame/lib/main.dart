import 'package:flame/flame.dart';
import 'package:flame/game.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';
import 'game.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Flame.device.fullScreen();
  await Flame.device.setPortraitUpOnly();

  await FlameAudio.audioCache.loadAll([
    'wing.mp3',
    'score.mp3',
    'crash.mp3',
  ]);

  runApp(
    GameWidget(
      game: FlappyPlaneGame(),
    ),
  );
}