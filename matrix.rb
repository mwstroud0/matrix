class Matrix < Formula
  desc "A Matrix-like rain effect written in Python"
  homepage "https://github.com/mwstroud0/matrix-rain"
  url "https://github.com/mwstroud0/matrix/archive/v1.0.tar.gz"
  sha256 "your_sha256_hash_here"  # Generate this after creating the tarball

  depends_on "python@3.10"

  def install
    bin.install "matrix"  # The executable launcher
    prefix.install "matrix.py"  # The main Python script

    # Ensure that the script can find the Python file
    (bin/"matrix").write <<~EOS
      #!/bin/bash
      python3 #{prefix}/matrix.py
    EOS
  end

  test do
    system "#{bin}/matrix", "--version"
  end
end