# pip install pygraphviz

import pygraphviz as pgv

# Create a new graph
graph = pgv.AGraph(directed=True)

# Add nodes
graph.add_node('user', label='user\n- user_id (PK)\n- username\n- email\n- created_at')
graph.add_node('music', label='music\n- music_id (PK)\n- title\n- artist\n- created_at')
graph.add_node('comment', label='comment\n- comment_id (PK)\n- music_id (FK)\n- user_id (FK)\n- content\n- created_at')
graph.add_node('likes', label='likes\n- user_id (FK)\n- music_id (FK)\n- liked_at')
graph.add_node('notification', label='notification\n- notification_id (PK)\n- user_id (FK)\n- music_id (FK)\n- message\n- is_read\n- created_at')

# Add edges
graph.add_edge('user', 'comment')
graph.add_edge('music', 'comment')
graph.add_edge('user', 'likes')
graph.add_edge('music', 'likes')
graph.add_edge('user', 'notification')
graph.add_edge('music', 'notification')

# Render the graph
graph.layout(prog='dot')
graph.draw('erd_diagram.png')
