from setuptools import setup, find_packages

setup(
    name='sqlvana',
    version='0.1.1',
    package_dir={'': 'src'},  # 告诉setuptools包的实际位置  
    packages=find_packages(where='src'),  # 从src目录查找包  
    install_requires=[
         "requests", "tabulate", "plotly", "pandas", "sqlparse", "kaleido", "flask", "sqlalchemy"
    ],
    author='fomo3d',
    author_email='fomo3d.wiki@gmail.com',
    description='SQL自然语言可视化查询',
    license='MIT',
    keywords='SQL 自然语言 可视化 查询',
    url='https://github.com/chuangyeshuo/sqlvana'
)