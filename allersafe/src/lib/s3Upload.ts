/**
 * S3 upload utility functions for client-side uploads
 */

import { dataUrlToBlob, generateUniqueFilename, getExtensionFromDataUrl } from './imageUtils'

interface PresignedUrlResponse {
  uploadUrl: string  // Presigned HTTPS URL for uploading
  key: string        // S3 object key (path within bucket)
  publicUrl: string  // S3 URI path (s3://bucket/key format)
}

/**
 * Request a presigned URL from the API
 * @param filename - Name of the file to upload
 * @param contentType - MIME type of the file
 * @returns Presigned URL data
 */
async function requestPresignedUrl(filename: string, contentType: string): Promise<PresignedUrlResponse> {
  const response = await fetch('/api/upload-url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      filename,
      contentType,
    }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to get upload URL')
  }

  return response.json()
}

/**
 * Upload a blob to S3 using presigned URL
 * @param blob - Blob to upload
 * @param uploadUrl - Presigned S3 URL
 * @param contentType - MIME type
 * @param onProgress - Optional progress callback
 */
async function uploadBlobToS3(
  blob: Blob,
  uploadUrl: string,
  contentType: string,
  onProgress?: (progress: number) => void
): Promise<void> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()

    // Track upload progress
    if (onProgress) {
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const progress = (e.loaded / e.total) * 100
          onProgress(progress)
        }
      })
    }

    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        resolve()
      } else {
        reject(new Error(`Upload failed with status ${xhr.status}`))
      }
    })

    xhr.addEventListener('error', () => {
      reject(new Error('Upload failed'))
    })

    xhr.addEventListener('abort', () => {
      reject(new Error('Upload aborted'))
    })

    xhr.open('PUT', uploadUrl)
    xhr.setRequestHeader('Content-Type', contentType)
    xhr.send(blob)
  })
}

/**
 * Upload image data URL to S3
 * @param dataUrl - Base64 data URL
 * @param prefix - Optional filename prefix
 * @param onProgress - Optional progress callback (0-100)
 * @returns S3 URI path of uploaded image (e.g., s3://bucket/uploads/file.jpg)
 */
export async function uploadImageToS3(
  dataUrl: string,
  prefix: string = 'product',
  onProgress?: (progress: number) => void
): Promise<string> {
  try {
    // Convert data URL to blob
    const blob = dataUrlToBlob(dataUrl)
    const extension = getExtensionFromDataUrl(dataUrl)
    const filename = generateUniqueFilename(prefix, extension)
    const contentType = blob.type

    // Get presigned URL
    const { uploadUrl, publicUrl } = await requestPresignedUrl(filename, contentType)

    // Upload to S3
    await uploadBlobToS3(blob, uploadUrl, contentType, onProgress)

    return publicUrl
  } catch (error) {
    console.error('S3 upload error:', error)
    throw error
  }
}
