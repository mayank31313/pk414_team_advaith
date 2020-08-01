import { Kuzzle, WebSocket, Collection} from 'kuzzle-sdk';
const kuzzle = new Kuzzle(new WebSocket('172.16.221.11'));

async function connect(){
    try {
        await kuzzle.connect();
    
        const expiresIn = '1h';
        const credentials = {
            username: 'mayank31313',
            password: 'lovemylife'
        };
        
        await kuzzle.auth.login('local', credentials, expiresIn);
        console.log('Successfully connected');

        await kuzzle.realtime.subscribe("sih", "goverment-all",{},function(notification){
            console.log(notification)
        })
    } catch (error) {
        console.log(error.message);
  }
}

connect()
export {kuzzle}