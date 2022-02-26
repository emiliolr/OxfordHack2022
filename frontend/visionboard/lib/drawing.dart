import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:visionboard/shape.dart';
import 'dart:math';
import 'constants.dart';
import 'dart:ui';

import 'hexcolor.dart';

// Widget
Widget Drawing(context, List<MyShape> itemsToDraw) {
  return Container(
    decoration: const BoxDecoration(
        color: BLUE_DARK2, borderRadius: BorderRadius.all(Radius.circular(20))),
    width: MediaQuery.of(context).size.width,
    padding: EdgeInsets.all(16.0),
    margin: EdgeInsets.all(16.0),
    child: CustomPaint(
      painter: OpenPainter(itemsToDraw: itemsToDraw),
    ),
  );
}

// Draw on our canvas
class OpenPainter extends CustomPainter {
  List<MyShape> itemsToDraw;

  OpenPainter({required this.itemsToDraw});

  Paint get_paint(String color, bool fill){
    Color paintColor = HexColor(color);

    return Paint()
      ..style = fill ? PaintingStyle.fill : PaintingStyle.stroke
      ..strokeWidth = 5.0
      ..color = paintColor
      ..isAntiAlias = true;
  }

  void draw_rectangle(Canvas canvas, Rectangle rectangle){
    Paint paint = get_paint(rectangle.color, rectangle.fill);
    canvas.drawRect(Rect.fromLTWH(rectangle.x_start, rectangle.y_start, rectangle.width, rectangle.height), paint);
  }

  void draw_circle(Canvas canvas, Circle circle){
    Paint paint = get_paint(circle.color, circle.fill);
    canvas.drawCircle(Offset(circle.x_center, circle.y_center), circle.radius, paint);
  }

  @override
  void paint(Canvas canvas, Size size) {

    if (size.width > 1.0 && size.height > 1.0) {
      print(">1.9");
      SizeUtil.size = size;
    }

    itemsToDraw.forEach((MyShape shape){
      print(shape);
      if(shape.shapeName == 'circle'){
        draw_circle(canvas, shape as Circle);
      }
      else if(shape.shapeName == 'rectangle'){
        draw_rectangle(canvas, shape as Rectangle);
      }
    });

    canvas.save();
    canvas.restore();
  }

  @override
  bool shouldRepaint(OpenPainter oldDelegate) => oldDelegate.itemsToDraw != itemsToDraw;
}









// This will allow us to map our drawing to different device sizes
class SizeUtil {
  static const _DESIGN_WIDTH = 1000;
  static const _DESIGN_HEIGHT = 1000;

  //logic size in device
  static Size _logicSize = Size(200, 200);

  //device pixel radio.

  static get width {
    return _logicSize.width;
  }

  static get height {
    return _logicSize.height;
  }

  static set size(size) {
    _logicSize = size;
  }

  //@param w is the design w;
  static double getAxisX(double w) {
    return (w * width) / _DESIGN_WIDTH;
  }

// the y direction
  static double getAxisY(double h) {
    return (h * height) / _DESIGN_HEIGHT;
  }

  // diagonal direction value with design size s.
  static double getAxisBoth(double s) {
    return s *
        sqrt((width * width + height * height) /
            (_DESIGN_WIDTH * _DESIGN_WIDTH + _DESIGN_HEIGHT * _DESIGN_HEIGHT));
  }
}
