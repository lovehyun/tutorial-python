# 필요한 라이브러리 설치 - 윈도우에 graphviz 별도 설치 필요
# pip install pygraphviz
#
# 다이어그램 자동으로 그려주는 도구
# pip install eralchemy
# eralchemy -i sqlite:///database/music.db -o erd_diagram.png
# eralchemy -i mysql+pymysql://username:password@hostname/database_name -o erd_diagram.png

import pygraphviz as pgv

# Create a new graph
graph = pgv.AGraph(directed=True)

# Add nodes
graph.add_node('user', label='user\n- user_id (PK)\n- username\n- password\n- email\n- created_at')
graph.add_node('music', label='music\n- music_id (PK)\n- title\n- artist\n- album_image\n- created_at')
graph.add_node('comment', label='comment\n- comment_id (PK)\n- music_id (FK)\n- user_id (FK)\n- content\n- created_at')
graph.add_node('like', label='like\n- like_id (PK)\n- user_id (FK)\n- music_id (FK)')

# Add edges
graph.add_edge('user', 'comment')
graph.add_edge('music', 'comment')
graph.add_edge('user', 'like')
graph.add_edge('music', 'like')

# Render the graph
graph.layout(prog='dot')
graph.draw('erd_diagram.png')
