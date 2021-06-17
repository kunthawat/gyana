import { Controller } from 'stimulus'
import GoogleUploader from '../upload'
import { getApiClient } from '../api'

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

      const container = document.getElementById('global-upload-container')
      container.className = 'border border-gray-50 rounded-sm bg-white'
      Object.assign(container.style, styles)
    }
  }

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
      Turbo.visit(this.redirectToValue)
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
