import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

class FlappyPlaneGame extends FlameGame with TapDetector {
  late SpriteComponent plane;
  late TextComponent scoreText;
  late List<CloudPair> clouds;
  double velocity = 0;
  double lift = -300;
  double planeY = 0;
  int score = 0;
  bool isGameOver = false;

  @override
  Future<void> onLoad() async {
    camera.viewport = FixedResolutionViewport(Vector2(400, 600));

    final planeSprite = await loadSprite('plane.png');
    plane = SpriteComponent(
      sprite: planeSprite,
      size: Vector2(40, 20),
      position: Vector2(100, 300),
    );
    add(plane);
    planeY = plane.y;

    scoreText = TextComponent(
      text: '0',
      textRenderer: TextPaint(
        style: const TextStyle(fontSize: 32, color: Colors.black),
      ),
      position: Vector2(200, 50),
    );
    add(scoreText);

    clouds = [];
    isGameOver = false;
  }

  @override
  void update(double dt) {
    if (isGameOver) return;

    velocity += 500 * dt;
    planeY += velocity * dt;
    plane.y = planeY;

    if (clouds.isEmpty || clouds.last.x < 300) {
      spawnCloud();
    }

    final toRemove = <CloudPair>[];
    for (final cloud in clouds) {
      cloud.update(dt);
      if (cloud.x < -100) {
        toRemove.add(cloud);
      }
      if (cloud.collidesWithComponent(plane)) {
        endGame();
      }
    }
    clouds.removeWhere((c) => toRemove.contains(c));

    if (planeY < 0 || planeY > 600) {
      endGame();
    }

    super.update(dt);
  }

  void spawnCloud() {
    final gap = 160.0;
    final topHeight = Random().nextInt(200) + 100.0;
    final cloud = CloudPair(
      x: 400,
      topHeight: topHeight,
      gap: gap,
    );
    add(cloud);
    clouds.add(cloud);
  }

  @override
  void onTap() {
    if (!isGameOver) {
      velocity = lift;
      FlameAudio.play('wing.mp3');
    }
  }

  void endGame() {
    if (isGameOver) return;
    isGameOver = true;
    FlameAudio.play('crash.mp3');
    // Можно добавить оверлей: "Game Over"
    Future.delayed(Duration(seconds: 1), () {
      // Перезапуск: вызов restart() извне
    });
  }

  void incrementScore() {
    score++;
    scoreText.text = '$score';
    FlameAudio.play('score.mp3');
  }
}

class CloudPair extends PositionComponent {
  final double x;
  final double topHeight;
  final double gap;
  late SpriteComponent topCloud;
  late SpriteComponent bottomCloud;
  bool passed = false;

  CloudPair({required this.x, required this.topHeight, required this.gap})
      : super(position: Vector2(x, 0));

  @override
  Future<void> onLoad() async {
    final sprite = await gameRef.loadSprite('cloud.png');
    topCloud = SpriteComponent(
      sprite: sprite,
      size: Vector2(70, topHeight),
      position: Vector2(0, 0),
    );
    add(topCloud);

    bottomCloud = SpriteComponent(
      sprite: sprite,
      size: Vector2(70, 600 - topHeight - gap),
      position: Vector2(0, topHeight + gap),
    );
    add(bottomCloud);
  }

  void update(double dt) {
    position.x -= 150 * dt;
  }

  bool collidesWithComponent(Component other) {
    return toRect().overlaps(other.toRect());
  }

  double get x => position.x;

  @override
  Rect toRect() {
    return Rect.fromLTWH(
      x,
      0,
      70,
      topHeight,
    ).expandToInclude(
      Rect.fromLTWH(
        x,
        topHeight + gap,
        70,
        600 - topHeight - gap,
      ),
    );
  }
}