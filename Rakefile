def execute_command(command)
  puts(command)
  system(command)

  $?.exitstatus
end

def clean_workspace()
  execute_command('find . -name "*.pyc" -exec rm -rf {} \;')
  FileUtils.rm_rf('venv', :verbose => true) if Dir.exists?('venv')
end

file 'venv/bin/activate' do
  execute_command('virtualenv venv') unless Dir.exists?('venv')
end


task :clean do
  clean_workspace()
end

task :venv => ['requirements.txt', 'venv/bin/activate'] do
  execute_command('. venv/bin/activate; pip install -Ur requirements.txt')
end

task :test => [:venv] do
  execute_command('. venv/bin/activate; nosetests -v --with-gae ./tests/func')
end

task :build => [:clean, :venv, :test] do
  Rake::Task['clean'].reenable
  Rake::Task['clean'].invoke
end
