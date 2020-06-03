<template>
    <div>
        <el-drawer
            title="我是标题"
            direction="ltr"
            :visible.sync="drawer"
            :with-header="false"
            size="50%">    
            <p>
                文书制作单位
                <el-select v-model="options.wszzdw" clearable  placeholder="请选择">
                    <el-option
                        v-for="item in select[0]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </p>
            <p>
                文书种类
                <el-select v-model="options.fywszl" clearable placeholder="请选择">
                    <el-option
                        v-for="item in select[1]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </p>
            <p>
                法院级别
                <el-select v-model="options.fyjb" clearable placeholder="请选择">
                    <el-option
                        v-for="item in select[2]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </p>
            <p>
                行政区划 省
                <el-select v-model="options.xzqh_p" clearable placeholder="请选择">
                    <el-option
                        v-for="item in select[3]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </p>
            <!-- <p>
                行政区划 市
                <el-select v-model="options.xzqh_c" clearable placeholder="请选择">
                    <el-option
                        v-for="item in select[4]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </p> -->
            <p>
                案件类别
                <el-select v-model="options.ajlb" clearable placeholder="请选择">
                    <el-option
                        v-for="item in select[6]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </p>
            <p>
                审判程序
                <el-select v-model="options.spcx" clearable placeholder="请选择">
                    <el-option
                        v-for="item in select[7]"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
            </p>
            <!-- <p>
                判决时间
                <el-date-picker
                    v-model="date1"
                    type="daterange"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期">>
                </el-date-picker>
            </p> -->
        </el-drawer>
        <el-container>
            <el-header>
                <el-row>
                    <el-col :span="24">
                        <div class="grid-content title_clr">
                            <el-button
                            @click="drawer = true" 
                            icon="el-icon-collection-tag"
                            circle
                            class="ib"
                            >
                            </el-button>
                            <el-input 
                                :type="len"
                                class="searchinput" 
                                v-model="input" 
                                placeholder="搜索">
                                    
                            </el-input>
                            <el-button 

                            v-on:click="Search"
                            icon="el-icon-search"
                            circle
                            class="ib"
                            >
                            </el-button>
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-main>
                <div class="roll">
                    <ul
                    class="list"
                    v-infinite-scroll="load"
                    infinite-scroll-disabled="disabled">
                        <li 
                        v-for="(pp,i) in passages" 
                        :key="i" 
                        class="list-item">
                            <!-- <el-link 
                            :href="url" 
                            target="_blank">
                            {{pp}}
                            </el-link> -->
                            <el-button 
                            type="text" 
                            @click="go(pp.id)"
                            >{{pp.title}}</el-button>
                        </li>
                    </ul>
                </div>
            </el-main>
        </el-container>

    </div>  
</template>

<script>
export default {
    data() {
        return {
            options: {
                wszzdw:'',
                fywszl:'',
                xzqh_p:'',
                // xzqh_c:'',
                ajlb:'',
                // wszl:'',
                spcx:'',
            },
            sinvalue: '',
            mutvalue: '',
            date1:'',
            drawer: false,
            input: "",
            ph:"搜索内容",
            count: 10,
            loading: false,
            url:"s/",
            passages:[
            ],
            pagen:0,
            select:[],
            curkw:''
        }
    },
    props: {
    },
    mounted:function(){
        console.log('mounted')
        this.loading=true
        var url='lawinit/'
        var req = new XMLHttpRequest();
        req.open('GET', url, true);
        req.setRequestHeader("Content-type","application/json");
        req.send();
        var vue = this
        req.onreadystatechange = function () {
            console.log('init response')
            if (req.readyState == 4 && req.status == 200) {
                var json = req.responseText;
                // console.log(typeof(json));
                json = JSON.parse(json)
                // console.log(typeof(json));
                var i = 0
                for (var key in json) {
                    console.log(key);     //获取key值
                    // console.log(json[key]); //获取对应的value值
                    var oplist = []
                    for (var value of json[key]){
                        oplist.push({'value':value,'label':value})
                    }
                    var n = vue.select[i]=oplist
                    i+=1
                    console.log(n);
                }
            }
        };
    },
    computed: {
        len(){
            if (this.input.length>40){
                return 'textarea'
            }else{
                return ''
            }
        },
        noMore () {
            return this.count >= 100
        },
        disabled () {
            return this.loading || this.noMore
        },
        p_num(){
            return this.passages.length
        }
    },
    methods:{
        Search:function () {
            this.loading=false
            this.passages=[]
            var url='search/'
            console.log('Search for kw:' + this.input )
            var req = new XMLHttpRequest();
            req.open('POST', url, true);
            req.setRequestHeader("Content-type","application/json");
            var obj = this.options
            
            obj['kw']=this.input
            this.curkw=this.input
            obj['pagen']=0
            this.pagen=1
            console.log(JSON.stringify(obj))
            req.send(JSON.stringify(obj));

            var vue = this
            req.onreadystatechange = function () {
                console.log('response')

                if (req.readyState == 4 && req.status == 200) {
                    var json = req.responseText;
                    json = JSON.parse(json)
                    var answer = json['passage']
                    console.log('ans:')
                    console.log(answer)
                    console.log('vue.pass')
                    console.log(vue.passages)
                    for (var i in answer){
                        vue.passages.push(answer[i])
                    }
                    console.log('vue.pass')
                    console.log(vue.passages)
                }
            };
        },
        load () {
            console.log('load',this.count)
            this.loading = true
            var url='search/'
            console.log('load')
            var req = new XMLHttpRequest();
            req.open('POST', url, true);
            req.setRequestHeader("Content-type","application/json");
            var obj = this.options

            obj['kw']=this.curkw
            obj['pagen']=this.pagen
            console.log(JSON.stringify(obj))
            req.send(JSON.stringify(obj));

            var vue = this
            req.onreadystatechange = function () {
                console.log('response')
                if (req.readyState == 4 && req.status == 200) {
                    var json = req.responseText;
                    json = JSON.parse(json)
                    var answer = json['passage']
                    for (var i in answer){
                        vue.passages.push(answer[i])
                    }
                }
            }
            setTimeout(() => {
                this.pagen += 1
                this.loading = false
            },2000)
        },
        go(xmlid){
            console.log('visit passage',xmlid)
            // this.loading = true
            var url='p/'+xmlid.toString()+'/'
            console.log('load')
            var req = new XMLHttpRequest();
            req.open('GET', url, true);
            req.setRequestHeader("Content-type","application/json");
            req.send()
            // var obj = this.options
            
            // obj['pass']=xmlid
            // obj['kw']=this.curkw
            // obj['pagen']=this.pagen
            // console.log(JSON.stringify(obj))
            // req.send(JSON.stringify(obj));x
            var pre = window.location.href
            console.log(pre)
            url = pre + url
            req.onreadystatechange = function () {
                console.log('response')
                if (req.readyState == 4 && req.status == 200) {
                    // var html = req.responseText;
                    window.open(url);
                    // newWindow.document.write(html);
                }
            }
        }
    }
}
</script>

<style scoped>
    .el-header{
        height: 60px;
        padding:0;
    }
    .el-main{
        padding: 0;

    }
    .el-container{
        height: 100vh;
    }
    .el-row {
        height: 100%;
        
    }
    .el-col {
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .title_clr {
        background: #1d5cb4;
    }
    .grid-content {

        height: 100%;
        /* padding-top:10px; */
    }
    .searchinput{
        margin-top:10px;
        margin-bottom:10px;
        max-width: 80%;
        min-height: 40px;
        /* width:95%; */
    }
    .roll{
        height: 100%;
        overflow: auto;

    }
    .list{
        height: 100%;
        margin: 0;
        padding: 0;
        overflow:auto;

    }
    .list-item{
        height: 10%;
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        list-style: none;
        width:70%;
        margin: 0 15% 0 15%;
    }
    .ib{
        margin: 0 20px 0 20px;
    }
</style>