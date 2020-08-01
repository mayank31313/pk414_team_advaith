<template>
    <q-page 
    ref="pageChat"
    class="flex column page-chat full-width">
  <div 
  :class=" { 'invisible' : !showMessages }"
  class="q-pa-md column col justify-end">
      <q-chat-message
      v-for="(message, key) in messages"
        :key="key"
        :text="[message.text]"
        :sent = "message.from =='me' ? true : false"
        :bg-color="message.from =='me' ? 'white' : 'light-green-2'"
      />
    </div>
  <q-footer >
      <q-toolbar>
        <!-- <q-form class="full-width"> -->
            <q-input 
            ref="message"
            v-model="newMessage" 
            label="Type Your Message" 
            class="full-width q-pa-sm"
            bg-color="white"
            outlined
            rounded
            @keyup.enter="sendMessage"
            dense
            >
            <template v-slot:after>
              <q-btn 
              round 
              dense 
              flat 
              @click="sendMessage"
              icon="send" 
              color="white"
              class="bg-green-14"
              />
            </template>
          </q-input>
        <!-- </q-form> -->
      </q-toolbar>
      </q-footer>
  </q-page>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  created(){
    let token = window.localStorage.getItem('token')
    if(!token){
      this.$router.push('/')
    }
  },
  data(){
    return{
      newMessage:'',
      showMessages:false
    }
  },
  computed:{
    ...mapState('store', ['messages'])
  },
  methods:{
    ...mapActions('store',['firebaseGetMessages','firebaseStopGettingMessages', 'firebaseSendMessage']),
    sendMessage(){
        this.firebaseSendMessage({
          message:{text:this.newMessage,
          from:'me'
          },
          otheruserid:this.$route.params.id
        })
        this.clearMessage()   
    },
    clearMessage(){
      this.newMessage = ''
    },
    scrollToBottom(){
      let pageChat = this.$refs.pageChat.$el
      setTimeout(() => {
        window.scrollTo(0 , pageChat.scrollHeight)
      }, 20 );
    }
  },
  watch:{
    messages: function(val) {
      if(Object.keys(val).length){
        this.scrollToBottom()
        setTimeout(() => {
          this.showMessages = true
        }, 100);
      }
    }
  },
  mounted(){
    this.firebaseGetMessages(this.$route.params.id)
  },
  destroyed(){
    this.firebaseStopGettingMessages()
  }
}
</script>
<style lang="stylus">
  .page-chat
    background #e2dfd5
    &:after
      content ''
      display block
      position fixed
      left 0
      right 0
      top 0
      bottom 0
      z-index 0
      opacity 0.2
      background radial-gradient(circle farthest-side at 0% 50%,#fb1 23.5%,rgba(240,166,17,0) 0)21px 30px,
          radial-gradient(circle farthest-side at 0% 50%,#B71 24%,rgba(240,166,17,0) 0)19px 30px,
          linear-gradient(#fb1 14%,rgba(240,166,17,0) 0, rgba(240,166,17,0) 85%,#fb1 0)0 0,
          linear-gradient(150deg,#fb1 24%,#B71 0,#B71 26%,rgba(240,166,17,0) 0,rgba(240,166,17,0) 74%,#B71 0,#B71 76%,#fb1 0)0 0,
          linear-gradient(30deg,#fb1 24%,#B71 0,#B71 26%,rgba(240,166,17,0) 0,rgba(240,166,17,0) 74%,#B71 0,#B71 76%,#fb1 0)0 0,
          linear-gradient(90deg,#B71 2%,#fb1 0,#fb1 98%,#B71 0%)0 0 #fb1
      background-size 40px 60px
  .q-message
    z-index 1 
</style>