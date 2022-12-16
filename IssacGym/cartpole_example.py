class CartPole(BaseTasks):
    # common callbacks
    def create_sim(self):
        """create environemnts and actors"""
    
    def pre_physics_step(self, actions):
        """apply actions"""

    def post_physics_step(self):
        """compute observations, rewards, and resets"""

    def compute_observations(self):
        # refresh state tensor
        self.gym.refresh_dof_state_tensor(self.sim)

        # copy DOF states to observation tensor
        self.obs_buf[:, 0] = self.dof_pos[:, 0]
        self.obs_buf[:, 1] = self.dof_pos[:, 0]
        self.obs_buf[:, 2] = self.dof_pos[:, 1]
        self.obs_buf[:, 2] = self.dof_pos[:, 1]

    def compute_reward(self):
        cart_pos = self.obs_buf[:, 0]
        cart_vel = self.obs_buf[:, 1]
        pole_angle = self.obs_buf[:, 2]
        pole_vel = self.obs_buf[:,3]

        self.rew_buf[:] = compute_cartpole_reward(cart_pos, cart_vel, pole_angle, pole_vel)

    # use the torchsript JIT compiler to run computations on the GPU

    @torch.jit.script
    def compute_cartpole_reward(cart_pos, cart_vel, pole_angle, pole_vel):
        # type: (tensor, tensor ,tensor, tensor) -> tensor

        angle_penalty = pole_angle * pole_angle
        vel_penalty = 0.01 * torch.abs(cart_vel) - 0.005 * torch.abs(pole_vel)

        return 1.0 - angle_penalty - vel_penalty

    # apply acitons

    def pre_physics_step(self, actions):

        # prepare DOF force sensr
        forces = torch.zeros((num_envs, dofs_per_env), dtype=torch.float32, device=self.device)

        # scale actions and write to cart DOF slice
        forces[:, 0] = actions * self.max_push_force

        # apply the forces to all actors
        self.gym.set_dof_actuation_force_tesnsor(self.sim, gymtorch.unwrap_tensor(forces))

    # resetting selected environemnts

    def reset(self, env_ids):

        #number of environemnts to reset
        num_reset = len(env_ids)

        # generate rnadom DOF positions and velocities
        p = 0.3 * (torch.rand((num_resets, dofs_per_env), device=self.device) - 0.5)
        v = 0.5 * (torch.rand((num_resets, dofs_per_env), device=self.device) - 0.5)

        # write new states to DOF state tensor
        self.dof_states[env_ids, 0] = p
        self.dof_states[env_ids, 1] = v
        
        # apply the new dof states for selected envs using env_ids as the actor index tensor
        self.gym.set_dof_state_tensor_indexed(self.sim, self.dof_state_desc, gymtorch.unwrap_tensor(env_ids), num_resets)