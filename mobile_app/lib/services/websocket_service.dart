import 'dart:convert';
import 'dart:async';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:shared_preferences/shared_preferences.dart';

class WebSocketService extends ChangeNotifier {
  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  bool _isConnected = false;
  String? _userId;

  bool get isConnected => _isConnected;

  Future<void> connect(String userId) async {
    _userId = userId;
    try {
      _channel = WebSocketChannel.connect(
        Uri.parse('ws://localhost:8000/ws/$userId'), // Change to your server IP
      );
      
      _subscription = _channel!.stream.listen(
        (data) {
          _handleMessage(data);
        },
        onError: (error) {
          print('WebSocket error: $error');
          _isConnected = false;
          notifyListeners();
        },
        onDone: () {
          print('WebSocket connection closed');
          _isConnected = false;
          notifyListeners();
        },
      );
      
      _isConnected = true;
      notifyListeners();
    } catch (e) {
      print('Failed to connect to WebSocket: $e');
      _isConnected = false;
      notifyListeners();
    }
  }

  void _handleMessage(String data) {
    try {
      final message = json.decode(data);
      print('Received WebSocket message: $message');
      
      // Handle different message types
      switch (message['type']) {
        case 'order_created':
          _handleOrderCreated(message);
          break;
        case 'order_paid':
          _handleOrderPaid(message);
          break;
        case 'table_status_changed':
          _handleTableStatusChanged(message);
          break;
        default:
          print('Unknown message type: ${message['type']}');
      }
    } catch (e) {
      print('Error parsing WebSocket message: $e');
    }
  }

  void _handleOrderCreated(Map<String, dynamic> message) {
    // Notify listeners about new order
    notifyListeners();
  }

  void _handleOrderPaid(Map<String, dynamic> message) {
    // Notify listeners about paid order
    notifyListeners();
  }

  void _handleTableStatusChanged(Map<String, dynamic> message) {
    // Notify listeners about table status change
    notifyListeners();
  }

  void disconnect() {
    _subscription?.cancel();
    _channel?.sink.close();
    _isConnected = false;
    _userId = null;
    notifyListeners();
  }

  @override
  void dispose() {
    disconnect();
    super.dispose();
  }
}
