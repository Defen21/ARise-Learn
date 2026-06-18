import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:edutech_mobile/main.dart';
import 'package:edutech_mobile/services/api_service.dart';

void main() {
  testWidgets('Smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(
      ChangeNotifierProvider(
        create: (_) => ApiService(),
        child: const EdutechApp(),
      ),
    );

    // Verify the app root exists.
    expect(find.byType(EdutechApp), findsOneWidget);
  });
}
