from autogen_agentchat.teams import RoundRobinGroupChat , SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination


# # Add simple helper functions for direct team operations
# def create_simple_db_team(db_agent):
#     """Create database team directly"""
#     return RoundRobinGroupChat(
#         [db_agent],
#         termination_condition=TextMentionTermination("TERMINATE") or MaxMessageTermination(10),
#     )

# def create_simple_visualization_team(visualization_agent):
#     """Create visualization team directly"""
#     return RoundRobinGroupChat(
#         [visualization_agent],
#         termination_condition=TextMentionTermination("TERMINATE") or MaxMessageTermination(10)
#     )



class TeamManager:
    """Manages agent teams and their interactions"""
    
    def __init__(self):
        self.db_team = None
        self.visualization_team = None
    
    def create_db_team(self, db_agent):
        """Create database team with termination conditions"""
        self.db_team = RoundRobinGroupChat(
            [db_agent],
            termination_condition=TextMentionTermination("TERMINATE") or MaxMessageTermination(10),
        )
        return self.db_team
    
    def create_visualization_team(self, visualization_agent):
        """Create visualization team with termination conditions"""
        self.visualization_team = RoundRobinGroupChat(
            [visualization_agent],
            termination_condition=TextMentionTermination("TERMINATE") or MaxMessageTermination(10)
        )
        return self.visualization_team
    
    def create_data_analysis_team(self, openai_client, DataAnalysisExpert,code_executor_agent,human_agent, ):
        """Create visualization team with termination conditions"""
        self.data_analysis_team  = SelectorGroupChat(
            participants=[DataAnalysisExpert, code_executor_agent,human_agent],
            termination_condition= TextMentionTermination('STOP') or MaxMessageTermination(15),
            model_client=openai_client,
            )
        return self.data_analysis_team
    
    async def reset_data_analysis_team(self):
        """Reset only the database team"""
        if self.data_analysis_team:
            await self.data_analysis_team.reset()

    async def reset_db_team(self):
        """Reset only the database team"""
        if self.db_team:
            await self.db_team.reset()
    
    async def reset_visualization_team(self):
        """Reset only the visualization team"""
        if self.visualization_team:
            await self.visualization_team.reset()
    
    async def reset_teams(self):
        """Reset all teams"""
        if self.db_team:
            await self.db_team.reset()
        if self.visualization_team:
            await self.visualization_team.reset()
    


