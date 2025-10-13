import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import 'captain_screens/tables_screen.dart';
import 'admin_screens/dashboard_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthService>(
      builder: (context, authService, child) {
        final user = authService.user!;
        
        return Scaffold(
          appBar: AppBar(
            title: Text('HUNGER Restaurant'),
            backgroundColor: Colors.orange.shade600,
            actions: [
              PopupMenuButton<String>(
                onSelected: (value) {
                  if (value == 'logout') {
                    authService.logout();
                  }
                },
                itemBuilder: (BuildContext context) => [
                  PopupMenuItem<String>(
                    value: 'logout',
                    child: Row(
                      children: [
                        Icon(Icons.logout),
                        SizedBox(width: 8),
                        Text('Logout'),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
          body: _buildBody(user),
          bottomNavigationBar: _buildBottomNavigation(user),
        );
      },
    );
  }

  Widget _buildBody(User user) {
    switch (user.role) {
      case 'CAPTAIN':
        return _buildCaptainBody();
      case 'ADMIN':
      case 'SUPER_ADMIN':
        return _buildAdminBody();
      default:
        return Center(child: Text('Unknown role: ${user.role}'));
    }
  }

  Widget _buildCaptainBody() {
    switch (_selectedIndex) {
      case 0:
        return TablesScreen();
      case 1:
        return Center(child: Text('Orders Screen - Coming Soon'));
      default:
        return Center(child: Text('Unknown screen'));
    }
  }

  Widget _buildAdminBody() {
    switch (_selectedIndex) {
      case 0:
        return DashboardScreen();
      case 1:
        return Center(child: Text('Menu Management - Coming Soon'));
      case 2:
        return Center(child: Text('User Management - Coming Soon'));
      default:
        return Center(child: Text('Unknown screen'));
    }
  }

  Widget _buildBottomNavigation(User user) {
    if (user.role == 'CAPTAIN') {
      return BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.table_restaurant),
            label: 'Tables',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.receipt_long),
            label: 'Orders',
          ),
        ],
      );
    } else {
      return BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: 'Dashboard',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.restaurant_menu),
            label: 'Menu',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Users',
          ),
        ],
      );
    }
  }
}
