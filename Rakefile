def execute_command(command)
  puts(command)
  system(command)

  $?.exitstatus
end

file 'venv/bin/activate' do
  execute_command('virtualenv venv') unless Dir.exists?('venv')
end


task :clean do
  execute_command('find . -name "*.pyc" -exec rm -rf {} \;')
  FileUtils.rm_rf('venv', :verbose => true) if Dir.exists?('venv')
end

task :venv => ['requirements.txt', 'venv/bin/activate'] do
  execute_command('. venv/bin/activate; pip install -Ur requirements.txt')
end

task :build => [:venv] do
  execute_command('. venv/bin/activate; nosetests -v --with-gae ./tests/func')
end
