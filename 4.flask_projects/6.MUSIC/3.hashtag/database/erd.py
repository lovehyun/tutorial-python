# 필요한 라이브러리 설치 - 윈도우에 graphviz 별도 설치 필요
# pip install pygraphviz
# pip install pygraphviz --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib"

# 다이어그램 자동으로 그려주는 도구 (SQLAlchemy와 버전이 맞아야 함. 현재 1.3.x 까지만 지원함.)
# pip install eralchemy
# eralchemy -i sqlite:///music.db -o erd_diagram.png
# eralchemy -i mysql+pymysql://username:password@hostname/database_name -o erd_diagram.png

import pygraphviz as pgv

# Create a new graph with rectangular nodes
# graph = pgv.AGraph(directed=True, strict=True)

# Create a new graph with rectangular nodes and set the node and rank separation
# ranksep : 동일한 계층의 노드 간의 수직간격 (기본값: 0.5)
# nodesep : 동일한 계층에 있는 노드 간의 수평간격 (기본값: 0.25)
graph = pgv.AGraph(directed=True, strict=True, ranksep=1.0, nodesep=0.5)

# Add nodes with rectangle shapes
graph.add_node('user', label='user\n- user_id (PK)\n- username\n- password\n- email\n- created_at', shape='box')
graph.add_node('music', label='music\n- music_id (PK)\n- title\n- artist\n- album_image\n- created_at', shape='box')
graph.add_node('comment', label='comment\n- comment_id (PK)\n- music_id (FK)\n- user_id (FK)\n- content\n- created_at', shape='box')
graph.add_node('likes', label='likes\n- user_id (PK)\n- music_id (PK)\n- liked_at', shape='box')
graph.add_node('notification', label='notification\n- notification_id (PK)\n- user_id (FK)\n- music_id (FK)\n- comment_id (FK)\n- message\n- is_read\n- created_at', shape='box')
graph.add_node('hashtag', label='hashtag\n- hashtag_id (PK)\n- tag', shape='box')
graph.add_node('music_hashtag', label='music_hashtag\n- music_id (PK)\n- hashtag_id (PK)', shape='box')

# Add edges
graph.add_edge('user', 'comment', label='writes')
graph.add_edge('music', 'comment', label='has')
graph.add_edge('user', 'likes', label='likes')
graph.add_edge('music', 'likes', label='liked')
graph.add_edge('user', 'notification', label='receives')
graph.add_edge('music', 'notification', label='notifies')
graph.add_edge('comment', 'notification', label='triggers')
graph.add_edge('music', 'music_hashtag', label='tagged with')
graph.add_edge('hashtag', 'music_hashtag', label='tags')

# Render the graph
graph.layout(prog='dot')
graph.draw('erd_diagram.png')

print("ERD diagram has been generated and saved as 'erd_diagram.png'")
