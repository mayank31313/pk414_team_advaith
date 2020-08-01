<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { kuzzle } from './boot/kuzzle'

export default {
  name: 'App',
  created(){
    this.handleUserDetails()
    var token = window.localStorage.getItem('token')
    var username = window.localStorage.getItem('username')
    if(token){
      if(username==='0000000000'){
        this.$router.push('/admin')
      }
      else{
        this.$router.push('/home')
      }
    }
  },
  methods:{
    ...mapActions('store',['handleUserDetails'])
  }
}

</script>
