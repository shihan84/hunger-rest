class User {
  final String username;
  final String fullName;
  final String role;

  User({
    required this.username,
    required this.fullName,
    required this.role,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      username: json['username'],
      fullName: json['full_name'],
      role: json['role'],
    );
  }

  bool get isSuperAdmin => role == 'SUPER_ADMIN';
  bool get isAdmin => role == 'ADMIN' || isSuperAdmin;
  bool get isCaptain => role == 'CAPTAIN' || isAdmin;
}
