import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/menu_item.dart';
import '../models/order_item.dart';
import 'auth_service.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api'; // Change to your server IP
  final AuthService _authService;

  ApiService(this._authService);

  Map<String, String> get _headers {
    final token = _authService.token;
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  Future<List<MenuItem>> getMenuItems() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/menu'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => MenuItem.fromJson(item)).toList();
      } else {
        throw Exception('Failed to load menu items');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  Future<int> createMenuItem(MenuItem item) async {
    final response = await http.post(
      Uri.parse('$baseUrl/menu'),
      headers: _headers,
      body: json.encode({
        'name': item.name,
        'price': item.price,
        'category': item.category,
        'gst_slab': item.gstSlab,
        'hsn_code': item.hsnCode,
        'food_type': item.foodType,
      }),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['id'];
    } else {
      throw Exception('Failed to create item');
    }
  }

  Future<void> updateMenuItem(int id, MenuItem item) async {
    final response = await http.put(
      Uri.parse('$baseUrl/menu/$id'),
      headers: _headers,
      body: json.encode({
        'name': item.name,
        'price': item.price,
        'category': item.category,
        'gst_slab': item.gstSlab,
        'hsn_code': item.hsnCode,
        'food_type': item.foodType,
      }),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update item');
    }
  }

  Future<void> deleteMenuItem(int id) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/menu/$id'),
      headers: _headers,
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to delete item');
    }
  }

  Future<String> createOrder({
    required int tableNumber,
    required List<OrderItem> items,
    String? customerName,
    String? customerGstin,
    String? placeOfSupply,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/orders'),
        headers: _headers,
        body: json.encode({
          'table_number': tableNumber,
          'customer_name': customerName,
          'customer_gstin': customerGstin,
          'place_of_supply': placeOfSupply,
          'items': items.map((item) => item.toJson()).toList(),
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['invoice_number'];
      } else {
        throw Exception('Failed to create order');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }

  Future<bool> markOrderAsPaid(String invoiceNumber) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/orders/$invoiceNumber/paid'),
        headers: _headers,
      );

      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  Future<Map<String, dynamic>?> getOrderDetails(String invoiceNumber) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/orders/$invoiceNumber'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        return null;
      }
    } catch (e) {
      return null;
    }
  }

  Future<List<Map<String, dynamic>>> getOpenOrders() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/orders/open'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.cast<Map<String, dynamic>>();
      } else {
        return [];
      }
    } catch (e) {
      return [];
    }
  }
}
