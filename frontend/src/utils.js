export function formatTime(ms) {
  try {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  } catch (e) {
    return "3:00";
  }
}

export function slugify(value) {
  if (!value) return "";

  const slugified = value
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  return slugified || value.toLowerCase().replace(/\s+/g, "-");
}

export function deSlugify(value) {
  if (!value) return "";

  const deSlugified = value
    .replace(/-/g, " ")
    .replace(/_/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  return deSlugified || value;
}
