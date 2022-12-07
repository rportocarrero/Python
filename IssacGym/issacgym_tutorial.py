from issacgym import gymapi # core API
from issacgym import gymtorch # Pytorch Api

# set simulatio nparameters
sim_params = gymapi.SimParams()
sim_params.dt = 0.01
sim_params.physx.use_gpu = True

# enable GPU pipeline
sim_params.use_gpu_pipeline = True

# create new simulation
sim  = gym.create_sim(0, 0, gymapi.SIM_PHYSX, sim_params)

# prepare asssets
franka_asset = gym.load_asset(sim, "../assets", "urdf/franka.urdf", franka_options)
box_asset = gym.create_box(sim, 0.1, 0.1, 0.1, box_options)

# crete envs and add actors

for i in range(num_envs):
    
    #create new env
    env = gym.create_env(sim, ...)

    # create actors from assets
    franka = gym.create_actor(env, franka_asset, franka_pose, ...)
    box = gym.create_actor(env, box_asset, box_pose, ...)

    # configure initial poses, drives and other properties

# prepare simulation buffers and tensor storage - required to use the tensor API
gym.prepare_sim(sim)

# Acquire tensor descriptors
root_states_desc = gym.acquire_actor_root_state_tensor(sim)
dof_states_desc = gym.acquire_dof_state_tensor(sim)

# pytorch interop

root_states = gymtorch.wrap_tensor(root_states_desc)
dof_states = gymtorch.wrap_tensor(dof_states_desc)

# different views

root_states_vect = root_states.view(num_envs, actors_per_env, 13)
dof_states_vec = root_states.view(num_envs, dofs_per_env, 2)

# different slices

root_p = root_states_vec[..., 0:3]
root_q = root_states_vec[.., 3:7]
root_v = root_states_vec[...,7:10]
root_a = root_states_vec[...,10:13]

dof_p = dof_states_vec[..., 0]
dof_v = dof_states_vec[..., 1]


# simulation main loop
while True:

    #step the simulation
    gym.simulate(sim)

    # refresh state tensors

    gym.refresh_actor_root_state_tensor(sim)
    gym.refresh_dof_state_tensor(sim)

    # code to consume tensor data

# applying controls
forces = 1.0 - 2.0 * torch.rand((num_envs, dofs_per_env), dtype=torch.float32, device="cuda:0")

# use interop utility to cast pytorch tesnor to raw tensor discriptor
forces_desc = gymtorch.unwrap_tensor(forces)

# apply the forces
gym.set_dof_actuation_force_tensor(sim, forces_desc)

# can also use PD controls
gym.set_dof_position_target_tensor(sim, pos_targets_desc)
gym.set_dof_velocity_target_tensor(sim, vel_targets_desc)