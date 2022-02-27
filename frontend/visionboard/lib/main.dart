import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:http/http.dart' as http;
import 'package:visionboard/hexcolor.dart';
import 'package:visionboard/shape.dart';
import 'package:visionboard/shape_converter.dart';

import 'drawing.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SpokenVision',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        canvasColor: Colors.black87,
        fontFamily: 'Georgia',
      ),
      debugShowCheckedModeBanner: false,
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  SpeechToText _speechToText = SpeechToText();
  bool _speechEnabled = false;
  String _lastWords =
      'Please click the microphone to start creating...\nex. \"Give me a large red square.\"';
  List<MyShape> _itemsToDraw = [];

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }

  /////////////////////// Speech to text functions /////////////////////////

  /// This has to happen only once per app
  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize();
    setState(() {});
  }

  /// Each time to start a speech recognition session
  void _startListening() async {
    _lastWords = '';
    setState(() {});
    await _speechToText.listen(onResult: _onSpeechResult);
    setState(() {});
  }

  /// Manually stop the active speech recognition session
  /// Note that there are also timeouts that each platform enforces
  /// and the SpeechToText plugin supports setting timeouts on the
  /// listen method.
  void _stopListening() async {
    await _speechToText.stop();

    Response? response = await getLayout('$_lastWords');
    if (response != null) {
      Map<String, dynamic> output = jsonDecode(response.body);

      ShapeConverter myConverter = ShapeConverter(output);
      _itemsToDraw = _itemsToDraw + myConverter.getListOfShapes();
    } else {
      _lastWords = 'Nothing to show!';
    }
    setState(() {});
  }

  /// This is the callback that the SpeechToText plugin calls when
  /// the platform returns recognized words.
  void _onSpeechResult(SpeechRecognitionResult result) {
    setState(() {
      _lastWords = result.recognizedWords;
    });
  }

  Future<http.Response>? getLayout(String layout_description) {
    // TODO: Check that layout description is not empty or else don't call function
    if (layout_description.length > 1) {
      print('Calling cloud function with this text: ' + layout_description);
      return http.post(
        Uri.parse(
            'https://us-central1-visionboard-342516.cloudfunctions.net/get_layout'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
          'Access-Control-Allow-Origin': '*'
        },
        body: jsonEncode(<String, dynamic>{
          'text': layout_description + '.',
          'screen_width': (MediaQuery.of(context).size.width - 50.0).toInt(),
          'screen_height': (MediaQuery.of(context).size.height * 3 / 5).toInt(),
        }),
      );
    }
    return null;
  }

  ///////////////////////////// Canvas functions /////////////////////////////
  void clearCanvas() {
    print('Clearing canvas.');
    _itemsToDraw.clear();
    _lastWords =
        'Please click the microphone to start creating...\nex. \"Give me a large red square.\"';
    setState(() {});
  }

  void undo() {
    int index_of_last = _itemsToDraw.length - 1;
    if (index_of_last >= 0) {
      _itemsToDraw.remove(_itemsToDraw[index_of_last]);
    }
  }

  ///////////////////////////// Build widget tree /////////////////////////////

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('SpokenVision', style: TextStyle(fontSize: 32.0)),
      ),
      body: SafeArea(
          child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Stack(
              alignment: Alignment.bottomCenter,
              children: <Widget>[
                Container(
                    padding: EdgeInsets.only(bottom: 20.0),
                    child: Container(
                      decoration: BoxDecoration(
                        color: HexColor('#D9D9D9'),
                        border: Border.all(width: 6, color: Colors.greenAccent),
                        borderRadius: BorderRadius.all(
                          Radius.circular(15),
                        ),
                      ),
                      width: MediaQuery.of(context).size.width - 50.0,
                      height: MediaQuery.of(context).size.height * 3 / 5,
                      child: CustomPaint(
                        painter: OpenPainter(itemsToDraw: _itemsToDraw),
                      ),
                    )),
                Container(
                    margin: EdgeInsets.fromLTRB(40.0, 0.0, 40.0, 0.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        ClipOval(
                          child: Material(
                            color: Colors.greenAccent, // Button color
                            child: InkWell(
                              splashColor: Colors.green, // Splash color
                              onTap: () {
                                undo();
                              },
                              child: SizedBox(
                                  width: 45,
                                  height: 45,
                                  child: Icon(Icons.undo)),
                            ),
                          ),
                        ),
                        SizedBox(width: 10.0),
                        ClipOval(
                          child: Material(
                            color: Colors.greenAccent, // Button color
                            child: InkWell(
                              splashColor: Colors.green, // Splash color
                              onTap: () {
                                clearCanvas();
                              },
                              child: SizedBox(
                                  width: 45,
                                  height: 45,
                                  child: Icon(Icons.delete)),
                            ),
                          ),
                        ),
                        SizedBox(width: 10.0),
                        ClipOval(
                          child: Material(
                            color: Colors.greenAccent, // Button color
                            child: InkWell(
                              splashColor: Colors.green, // Splash color
                              onTap: () {
                                if (_speechToText.isNotListening) {
                                  _startListening();
                                } else {
                                  _stopListening();
                                }
                              },
                              child: SizedBox(
                                  width: 45,
                                  height: 45,
                                  child: Icon(_speechToText.isNotListening
                                      ? Icons.mic_off
                                      : Icons.mic)),
                            ),
                          ),
                        )
                      ],
                    ))
              ],
            ),
            Container(
                padding: EdgeInsets.all(16),
                child: SingleChildScrollView(
                    child: Column(
                  children: [
                    Text(
                      // If listening is active show the recognized words
                      _speechToText.isListening
                          ? '$_lastWords'
                          // If listening isn't active but could be tell the user
                          // how to start it, otherwise indicate that speech
                          // recognition is not yet ready or not supported on
                          // the target device
                          : _speechEnabled
                              ? '$_lastWords'
                              : 'Speech not available',
                      style: TextStyle(color: Colors.white, fontSize: 20),
                    ),
                  ],
                )))
          ],
        ),
      )),
    );
  }
}
