import { Controller } from 'stimulus'
import GoogleUploader from '../upload'
import { getApiClient } from '../api'

/**
 * Handles resumable uploads directly to GCS using signed urls
 *
 * Using the window javascript object as a state machine. Stimulus
 * controllers tend to reset and re-initialize throughout a user session,
 * the javascript window object stays alive.
 */
export default class extends Controller {
  static values = {
    fileInputId: String,
    fileId: String,
    redirectTo: String,
  }

  initialize() {
    if (!window.gyanaFileState) {
      // Prepare the state
      window.gyanaFileState = {}

      const styles = {
        display: 'block',
        position: 'absolute',
        right: '40px',
        bottom: '40px',
        width: '250px',
        minHeight: '150px',
      }

      // Set styles for the container, its only supposed to show up at our first
      // file upload.
      const container = document.getElementById('global-upload-container')
      container.className = 'border border-gray-50 rounded-sm bg-white'
      Object.assign(container.style, styles)
    }
  }

  /**
   * Main handler for starting a file upload
   *
   * The flow is as follows:
   * 1. Create a signed url in the backend
   * 2. Use this signed url to instantiate the uploader
   * 3. Hook in progress and success callbacks to update UI and trigger the sync on success
   *
   * Note: connect and disconnect are triggered every time the user changes route, we
   * need to carefully manage the registered listeners to avoid multiple callbacks.
   */
  async connect() {
    if (!window.gyanaFileState[this.fileIdValue]) {
      const file = document.getElementById(this.fileInputIdValue).files[0]

      const { url: target } = await getApiClient().action(
        window.schema,
        ['integrations', 'generate-signed-url', 'create'],
        {
          id: this.fileIdValue,
          filename: file.name,
        }
      )

      const uploader = (window.gyanaFileState[this.fileIdValue] = new GoogleUploader({
        target,
        file,
      }))

      uploader.start()
      // This redirect might be needed after we start the upload on a successful
      // integration create action.
      if (this.redirectToValue) Turbo.visit(this.redirectToValue)
    }

    const self = this
    this.progressCall = (progress) => {
      self.element.querySelector('#progress').innerHTML = progress
    }
    this.successCall = () => {
      getApiClient().action(window.schema, ['integrations', 'start-sync', 'create'], {
        id: this.fileIdValue,
      })
    }
    window.gyanaFileState[this.fileIdValue].on('progress', this.progressCall)
    window.gyanaFileState[this.fileIdValue].on('success', this.successCall)
  }

  disconnect() {
    window.gyanaFileState[this.fileIdValue].off(this.progressCall)
    window.gyanaFileState[this.fileIdValue].off(this.successCall)
  }
}
