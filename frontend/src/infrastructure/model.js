export function scoreToIcon(score) {
  if (score < 0.3) return "mdi-emoticon-dead";
  if (score < 0.5) return "mdi-emoticon-sad";
  if (score < 0.7) return "mdi-emoticon-neutral";
  if (score < 0.9) return "mdi-emoticon-happy";
  return "mdi-emoticon-excited";
}
