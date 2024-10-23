import { reactive } from "vue";
const paginationReactive = reactive({
	page: 1,
	pageSize: 20,
	showSizePicker: true,
	pageSizes: [10, 20, 50, 100],
	onChange: (page) => {
	  paginationReactive.page = page;
	},
	onUpdatePageSize: (pageSize) => {
	  paginationReactive.pageSize = pageSize;
	  paginationReactive.page = 1;
	}
});
export const pagination = paginationReactive;