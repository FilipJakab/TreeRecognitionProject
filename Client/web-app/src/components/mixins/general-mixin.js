import toastr from 'toastr'

import 'toastr/build/toastr.min.css'

export default {
	methods: {
		toastSuccess (body, title) {
			this.prepareToastr()
			
			toastr.success(body, title)
		},
		toastError (body, title) {
			this.prepareToastr()

			toastr.error(body, title)
		},
		prepareToastr () {
			toastr.options = {
				'closeButton': true,
				'debug': false,
				'positionClass': 'toast-top-center',
				'onclick': null,
				'showDuration': '1000',
				'hideDuration': '1000',
				'timeOut': '3500',
				'extendedTimeOut': '700',
				'showEasing': 'swing',
				'hideEasing': 'linear',
				'showMethod': 'fadeIn',
				'hideMethod': 'fadeOut'
			}
		}
	}
}
