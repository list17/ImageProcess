<template>
<div>
    <div style="width: 70%; margin:0 auto;">
        <el-table ref="filterTable"
            :data="datasetshow"
            highlight-current-row
            @selection-change="handleSelectionChange">
            <el-table-column
                type="selection"
                width="80">
            </el-table-column>
            <el-table-column
                prop="date"
                label="日期"
                sortable
                width="180"
                column-key="date"
                :filters="filter"
                :filter-method="filterHandler">
            </el-table-column>
            <el-table-column prop="id" label="ID" min-width="5%" >
            </el-table-column>
            <el-table-column prop="feature" label="进行的操作" min-width="10%" >
            </el-table-column>
            <el-table-column label="图片" min-width="40%" >
                <template slot-scope="scope" style="display:flex;justify-content:space-around ;">
                    <div style="display:flex; justify-content:space-between; width:100%;height:200px">
                        <div style="width:100%;height:200px">
                            <div>处理前</div>
                            <img :src="scope.row.image[0]"  width=90% />
                        </div>
                        <div style="width:100%;height:200px">
                            <div>处理后</div>
                            <img :src="scope.row.image[1]" width=90% />
                        </div>
                    </div>
                </template>
            </el-table-column>
            <el-table-column label="下载该次图片" min-width="10%">
                <template slot-scope="scope">
                    <el-button size="small" @click="handleEdit(scope.row)">下载</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            @current-change="handleCurrentChange"
            background
            layout="prev, pager, next"
            :page-size="10"
            :total="dataset.length">
        </el-pagination>
        <div style="margin-top: 20px">
            <el-button @click="deleterecords">删除选中记录</el-button>
            <el-button @click="toggleSelection()">取消选择</el-button>
        </div>
    </div>

</div>
</template>

<script>
  export default {
    name:'history',
    components:{

    },
    data() {
      return {
          dataset:[],
          datasetshow:[],
          filter:[],
          selection: [],
          currentItem:0,
          totalItems:0,
      }
    },
    mounted() {
        this.loadRecords()
    },
    methods: {
        loadRecords(){
            this.$axios.post('/filetransfer/download_user_history').then((response)=>{
                this.dataset = response.data.dataset;
                this.filter = response.data.filter;
                this.totalItems = this.dataset.length
                this.datasetshow = this.dataset.slice(0, 10<this.totalItems?10:this.totalItems)
            })
        },
        handleEdit(index){
            console.log(index)
            window.open('http://127.0.0.1:8080/api/filetransfer/download_file/?'+index['image'][1].split('?')[1],'_blank');
        },
        forceFileDownload(response){
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', 'file.png') //or any other extension
            document.body.appendChild(link)
            link.click()
        },
        filterHandler(value, row, column) {
            console.log(value, row, column);
            const property = column['property'];
            return row[property] === value;
        },
        // 清除选中的所有行
        toggleSelection(rows) {
            if (rows) {
                rows.forEach(row => {
                    this.$refs.filterTable.toggleRowSelection(row);
                });
            } else {
                this.$refs.filterTable.clearSelection();
            }
        },
        deleterecords(){
            let params = new URLSearchParams()
            let deletions = new Array()
            for(let i = 0; i < this.selection.length; i++){
                deletions.push(this.selection[i]['id'])
            }
            params.append('deleterecords', deletions)
            this.$axios.post('/filetransfer/deleterecords',params).then((response)=>{
                if(response.data['msg'] === "delete successfully"){
                    this.$confirm("删除成功").then(()=>{
                        this.loadRecords()
                    });
                }
            })
        },
        handleSelectionChange(val) {
            this.selection = val;
        },
        handleCurrentChange(val){
            this.currentItem = (val-1) * 10;
            this.datasetshow = this.dataset.slice(this.currentItem, (this.currentItem+10)<this.totalItems?(this.currentItem+10):this.totalItems)
        }
    }
  }

</script>

<style scoped>

</style>
