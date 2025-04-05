/**
 * Converts milliseconds to "minutes:seconds" format.
 * Example: 192000 => "3:12"
 */
export function msToMinutesSeconds(ms) {
  try {
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, "0")}`;
  } catch (e) {
    return "3:00"; // Default fallback
  }
}

export function customSlugify(value) {
  if (!value) return "";

  const slugified = value
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "") // Remove accents
    .replace(/[^a-z0-9]+/g, "-") // Replace non-alphanum with -
    .replace(/^-+|-+$/g, ""); // Trim - from ends

  return slugified || value.toLowerCase().replace(/\s+/g, "-");
}
