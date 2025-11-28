resource "aws_ecr_repository" "repo" {
  name                 = "log-rag-agent-repo"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

# Build and Push the Image
resource "docker_image" "agent_image" {
  name = "${aws_ecr_repository.repo.repository_url}:latest"
  
  build {
    context    = "../backend"   
    dockerfile = "Dockerfile"
    platform   = "linux/amd64"
  }
  
  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset("..", "*") : filesha1("../${f}")]))
  }
}

resource "docker_registry_image" "push" {
  name          = docker_image.agent_image.name
  keep_remotely = true
}