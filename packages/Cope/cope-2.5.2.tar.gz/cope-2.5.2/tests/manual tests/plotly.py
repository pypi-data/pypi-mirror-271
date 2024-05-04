from Cope.plotly import ridgeplot

# TODO: I have some tests for this somewhere...

#%%
# Just another visualization of the data
data = pl.DataFrame({
    'Avg. Reward': avg_reward_list,
    'Episode Length': ep_len_list,
    'Avg Actor Loss': ep_actor_loss,
    'Avg Critic Loss': ep_critic_loss,
})
# Add an index column
data = data.with_columns(Episode=pl.int_range(0, len(avg_reward_list)))
ridge = ridgeplot(data, x='Episode', z=['Avg. Reward', 'Episode Length', 'Avg Actor Loss', 'Avg Critic Loss'])
ridge
