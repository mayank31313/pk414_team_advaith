<template>
  <q-page class="flex q-pa-md">
   <q-list 
   class="full-width"
   separator>
      <q-item
       v-for="(user, key) in users" 
       :key="key"
       :to="'/chat/' + key"
       clickable 
       v-ripple>
        <q-item-section avatar>
          <q-skeleton type="QAvatar" v-if="load==false"/>
          <q-avatar v-else color="primary" text-color="white">
            {{ user.name.charAt(0) }}
          </q-avatar>
        </q-item-section>
        
        <q-item-section>
          <q-skeleton type="rect" width="100px" height="25px" v-if="load==false"/>
          <q-item-label v-else>{{ user.name }}</q-item-label>
        </q-item-section>

        <!-- <q-item-section side>
          <q-badge 
            :color="user.online ? 'light-green-5' : 'grey-4' " 
            >
            {{ user.online ? 'Online' : 'Offline' }}
          </q-badge>
        </q-item-section> -->
      </q-item>
    </q-list>
  </q-page>
</template>

<script>
import { mapGetters } from 'vuex'
let once = window.localStorage.getItem('once')
export default {
  created(){
    let token = window.localStorage.getItem('token')
    if(!token){
      this.$router.push('/')
    }
     setTimeout(() => {
       this.load = true
        }, 2000);
  },
  data () {
    return {
      load:false
    }
  },
  computed:{
      ...mapGetters('store',['users'])
  }
}
</script>
