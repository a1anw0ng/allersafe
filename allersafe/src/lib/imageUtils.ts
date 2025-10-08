/**
 * Image utility functions for converting between formats
 */

/**
 * Convert base64 data URL to Blob
 * @param dataUrl - Base64 data URL (e.g., "data:image/jpeg;base64,...")
 * @returns Blob object
 */
export function dataUrlToBlob(dataUrl: string): Blob {
  const arr = dataUrl.split(',')
  const mimeMatch = arr[0].match(/:(.*?);/)
  const mime = mimeMatch ? mimeMatch[1] : 'image/jpeg'
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n)
  }

  return new Blob([u8arr], { type: mime })
}

/**
 * Generate unique filename with timestamp and random string
 * @param prefix - Optional prefix for the filename
 * @param extension - File extension (default: 'jpg')
 * @returns Unique filename
 */
export function generateUniqueFilename(prefix: string = 'image', extension: string = 'jpg'): string {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(2, 9)
  return `${prefix}-${timestamp}-${random}.${extension}`
}

/**
 * Get file extension from data URL
 * @param dataUrl - Base64 data URL
 * @returns File extension (e.g., 'jpg', 'png')
 */
export function getExtensionFromDataUrl(dataUrl: string): string {
  const mimeMatch = dataUrl.match(/data:image\/(.*?);/)
  if (!mimeMatch) return 'jpg'

  const mime = mimeMatch[1]
  // Convert mime type to common extension
  const extensions: Record<string, string> = {
    'jpeg': 'jpg',
    'png': 'png',
    'gif': 'gif',
    'webp': 'webp'
  }

  return extensions[mime] || 'jpg'
}
