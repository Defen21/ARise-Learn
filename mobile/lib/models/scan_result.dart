class Recommendation {
  final String title;
  final String description;
  final String relevance;
  final String iconHint;

  Recommendation({
    required this.title,
    required this.description,
    this.relevance = 'Relevan',
    this.iconHint = 'book',
  });

  factory Recommendation.fromJson(Map<String, dynamic> json) {
    return Recommendation(
      title: json['title'] ?? 'Topik Terkait',
      description: json['description'] ?? '',
      relevance: json['relevance'] ?? 'Relevan',
      iconHint: json['icon_hint'] ?? 'book',
    );
  }
}

class ScanResult {
  final String id;
  final String explanation;
  final String subjectTopic;
  final double confidence;
  final String? asset3dUrl;
  final String? imageUrl;
  final List<Recommendation> recommendations;

  ScanResult({
    required this.id,
    required this.explanation,
    required this.subjectTopic,
    required this.confidence,
    this.asset3dUrl,
    this.imageUrl,
    this.recommendations = const [],
  });

  factory ScanResult.fromJson(Map<String, dynamic> json) {
    final data = json['data'] ?? json;
    final recsList = data['recommendations'] as List<dynamic>? ?? [];
    return ScanResult(
      id: data['id'] ?? '',
      explanation: data['explanation'] ?? '',
      subjectTopic: data['subject_topic'] ?? 'Unknown',
      confidence: (data['confidence'] ?? 0.0).toDouble(),
      asset3dUrl: data['asset_3d_url'],
      imageUrl: data['image_url'],
      recommendations: recsList
          .map((r) => Recommendation.fromJson(r as Map<String, dynamic>))
          .toList(),
    );
  }
}
