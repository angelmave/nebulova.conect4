from kaggle_environments import evaluate, make, utils
env = make("connectx", debug=True)

env.run(['random', 'random'])
env.render(mode="ipython", width=600, height=500, header=False)

def check_if_done(observation):
    done = [False,'No Winner Yet']
    #horizontal check
    for i in range(6):
        for j in range(4):
            if observation[i][j] == observation[i][j+1] == observation[i][j+2] == observation[i][j+3] == 1:
                done = [True,'Player 1 Wins Horizontal']
            if observation[i][j] == observation[i][j+1] == observation[i][j+2] == observation[i][j+3] == 2:
                done = [True,'Player 2 Wins Horizontal']
    #vertical check
    for j in range(7):
        for i in range(3):
            if observation[i][j] == observation[i+1][j] == observation[i+2][j] == observation[i+3][j] == 1:
                done = [True,'Player 1 Wins Vertical']
            if observation[i][j] == observation[i+1][j] == observation[i+2][j] == observation[i+3][j] == 2:
                done = [True,'Player 2 Wins Vertical']
    #diagonal check top left to bottom right
    for row in range(3):
        for col in range(4):
            if observation[row][col] == observation[row + 1][col + 1] == observation[row + 2][col + 2] == observation[row + 3][col + 3] == 1:
                done = [True,'Player 1 Wins Diagonal']
            if observation[row][col] == observation[row + 1][col + 1] == observation[row + 2][col + 2] == observation[row + 3][col + 3] == 2:
                done = [True,'Player 2 Wins Diagonal']
    
    #diagonal check bottom left to top right
    for row in range(5, 2, -1):
        for col in range(3):
            if observation[row][col] == observation[row - 1][col + 1] == observation[row - 2][col + 2] == observation[row - 3][col + 3] == 1:
                done = [True,'Player 1 Wins Diagonal']
            if observation[row][col] == observation[row - 1][col + 1] == observation[row - 2][col + 2] == observation[row - 3][col + 3] == 2:
                done = [True,'Player 2 Wins Diagonal']
    return done
def create_model():
    model = models.Sequential()
    
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    
    model.add(Dense(7))
    
    return model
   
def compute_loss(logits, actions, rewards): 
    neg_logprob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=actions)
    loss = tf.reduce_mean(neg_logprob * rewards)
    return loss
  
def train_step(model, optimizer, observations, actions, rewards):
    with tf.GradientTape() as tape:
      # Forward propagate through the agent network
        
        logits = model(observations)
        loss = compute_loss(logits, actions, rewards)
        grads = tape.gradient(loss, model.trainable_variables)
        
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

def get_action(model, observation, epsilon):
    #determine whether model action or random action based on epsilon
    act = np.random.choice(['model','random'], 1, p=[1-epsilon, epsilon])[0]
    observation = np.array(observation).reshape(1,6,7,1)
    logits = model.predict(observation)
    prob_weights = tf.nn.softmax(logits).numpy()
    
    if act == 'model':
        action = list(prob_weights[0]).index(max(prob_weights[0]))
    if act == 'random':
        action = np.random.choice(7)
        
    return action, prob_weights[0]

def check_if_action_valid(obs,action):
    if obs[action] == 0:
        
        valid = True
    else:
        valid = False
    return valid

def player_1_agent(observation, configuration):
    action, prob_weights = get_action(player_1_model,observation['board'],0)
    if check_if_action_valid(observation['board'],action):
        return action
    else:
        while True:
            previous_prob_weight = prob_weights[action]
            temp_prob = min(prob_weights)
            for prob in prob_weights:
                if prob < previous_prob_weight and prob > temp_prob:
                    temp_prob = prob
                    action = list(prob_weights).index(temp_prob)
            if check_if_action_valid(observation['board'],action):
                break
            
    return action

class Memory:
    def __init__(self): 
        self.clear()

    # Resets/restarts the memory buffer
    def clear(self): 
        self.observations = []
        self.actions = []
        self.rewards = []
        self.info = []
        
    def add_to_memory(self, new_observation, new_action, new_reward): 
        self.observations.append(new_observation)
        self.actions.append(new_action)
        self.rewards.append(float(new_reward))

#train player 1 against random agent
tf.keras.backend.set_floatx('float64')
optimizer = tf.keras.optimizers.Adam(LEARNING_RATE)

env = make("connectx", debug=True)
memory = Memory()
epsilon = 1

for i_episode in range(40000):
    
    trainer = env.train([None,'random'])
        
    observation = trainer.reset()['board']
    memory.clear()
    epsilon = epsilon * .99985
    overflow = False
    while True:
        action, _ = get_action(player_1_model,observation,epsilon)
        next_observation, dummy, overflow, info = trainer.step(action)
        observation = next_observation['board']
        observation = [float(i) for i in observation]
        done = check_if_done(np.array(observation).reshape(6,7))
        
        #-----Customize Rewards Here------
        if done[0] == False:
            reward = 0
        if 'Player 2' in done[1]:
            reward = -20
        if 'Player 1' in done[1]:
            win_count += 1
            reward = 20
        if overflow == True and done[0] == False:
            reward = -99
            done[0] = True
        #-----Customize Rewards Here------
        
        memory.add_to_memory(np.array(observation).reshape(6,7,1), action, reward)
        if done[0]:
            #train after each game
            
            train_step(player_2_model, optimizer,
                     observations=np.array(memory.observations),
                     actions=np.array(memory.actions),
                     rewards = memory.rewards)
            
            break


